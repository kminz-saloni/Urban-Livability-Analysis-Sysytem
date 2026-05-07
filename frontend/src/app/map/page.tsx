'use client'

import { useEffect, useRef, useState } from 'react'
import type { Map as MapLibreMap, Popup as MapLibrePopup, GeoJSONSource } from 'maplibre-gl'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { api } from '@/lib/api'
import LoadingSpinner from '@/components/common/LoadingSpinner'
import { MapPin, AlertTriangle, TrendingUp } from 'lucide-react'

type LivabilityFeatureProps = {
  city: string
  state: string
  score: number
  rank: number
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
}

export default function MapPage() {
  const router = useRouter()
  const mapContainerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<MapLibreMap | null>(null)
  const popupRef = useRef<MapLibrePopup | null>(null)
  const [isMapReady, setIsMapReady] = useState(false)
  const [mapError, setMapError] = useState<string | null>(null)
  const [activeLayers, setActiveLayers] = useState({
    aqi: false,
    crime: false,
    water: false,
  })

  const fallbackLivability: GeoJSON.FeatureCollection = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: { city: 'Kozhikode', state: 'Kerala', score: 78.5, rank: 1 },
        geometry: { type: 'Point', coordinates: [75.7804, 11.2588] },
      },
      {
        type: 'Feature',
        properties: { city: 'Delhi', state: 'Delhi', score: 52.1, rank: 24 },
        geometry: { type: 'Point', coordinates: [77.1025, 28.7041] },
      },
      {
        type: 'Feature',
        properties: { city: 'Patna', state: 'Bihar', score: 45.2, rank: 45 },
        geometry: { type: 'Point', coordinates: [85.1376, 25.5941] },
      },
    ],
  }

  useEffect(() => {
    const initMap = async () => {
      if (!mapContainerRef.current || mapRef.current) return
      const maplibregl = (await import('maplibre-gl')).default

      const map = new maplibregl.Map({
        container: mapContainerRef.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [78.9629, 20.5937],
        zoom: 4,
      })

      mapRef.current = map

      map.on('load', async () => {
        let geojson: GeoJSON.FeatureCollection = fallbackLivability
        try {
          const response = await api.getLivabilityMapData()
          if (response?.data?.features) {
            geojson = response.data as GeoJSON.FeatureCollection
          }
        } catch (error) {
          setMapError('Unable to reach the API. Showing fallback map data.')
        }

        map.addSource('livability', {
          type: 'geojson',
          data: geojson,
          cluster: true,
          clusterMaxZoom: 8,
          clusterRadius: 40,
        })

        map.addLayer({
          id: 'livability-clusters',
          type: 'circle',
          source: 'livability',
          filter: ['has', 'point_count'],
          paint: {
            'circle-radius': [
              'step',
              ['get', 'point_count'],
              14,
              5, 18,
              10, 22,
              20, 28,
            ],
            'circle-color': '#2563eb',
            'circle-opacity': 0.75,
            'circle-stroke-color': '#ffffff',
            'circle-stroke-width': 1,
          },
        })

        map.addLayer({
          id: 'livability-cluster-count',
          type: 'symbol',
          source: 'livability',
          filter: ['has', 'point_count'],
          layout: {
            'text-field': '{point_count_abbreviated}',
            'text-size': 12,
          },
          paint: {
            'text-color': '#ffffff',
          },
        })

        map.addLayer({
          id: 'livability-unclustered',
          type: 'circle',
          source: 'livability',
          filter: ['!', ['has', 'point_count']],
          paint: {
            'circle-radius': 8,
            'circle-color': [
              'step',
              ['get', 'score'],
              '#ef4444',
              45, '#f97316',
              55, '#eab308',
              65, '#3b82f6',
              75, '#22c55e',
            ],
            'circle-stroke-color': '#ffffff',
            'circle-stroke-width': 1,
          },
        })

        map.on('mouseenter', 'livability-unclustered', () => {
          map.getCanvas().style.cursor = 'pointer'
        })

        map.on('mousemove', 'livability-unclustered', (event) => {
          const feature = event.features?.[0]
          if (!feature) return

          const { city, state, score, rank } = feature.properties as LivabilityFeatureProps
          const html = `
            <div style="font-size:12px;line-height:1.3;">
              <div style="font-weight:600;">${city}, ${state}</div>
              <div>Score: ${Number(score).toFixed(1)}</div>
              <div>Rank: #${rank}</div>
            </div>
          `

          if (!popupRef.current) {
            popupRef.current = new maplibregl.Popup({
              closeButton: false,
              closeOnClick: false,
              offset: 12,
            })
          }

          const coordinates = (feature.geometry as GeoJSON.Point).coordinates as [number, number]
          popupRef.current.setLngLat(coordinates).setHTML(html).addTo(map)
        })

        map.on('mouseleave', 'livability-unclustered', () => {
          map.getCanvas().style.cursor = ''
          popupRef.current?.remove()
        })

        map.on('click', 'livability-unclustered', (event) => {
          const feature = event.features?.[0]
          const city = feature?.properties?.city as string | undefined
          if (!city) return
          const slug = city.toLowerCase().replace(/\s+/g, '-')
          router.push(`/profile/${slug}`)
        })

        map.on('click', 'livability-clusters', (event) => {
          const feature = event.features?.[0]
          const clusterId = feature?.properties?.cluster_id as number | undefined
          if (clusterId === undefined) return
          const source = map.getSource('livability') as GeoJSONSource
          source
            .getClusterExpansionZoom(clusterId)
            .then((zoom) => {
              const coordinates = (feature?.geometry as GeoJSON.Point).coordinates as [number, number]
              map.easeTo({ center: coordinates, zoom })
            })
            .catch(() => undefined)
        })

        setIsMapReady(true)
      })
    }

    initMap()

    return () => {
      popupRef.current?.remove()
      mapRef.current?.remove()
      mapRef.current = null
    }
  }, [router])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !isMapReady) return

    const ensureGeoJsonSource = (id: string, data: GeoJSON.FeatureCollection) => {
      if (map.getSource(id)) {
        const source = map.getSource(id) as GeoJSONSource
        source.setData(data)
        return
      }
      map.addSource(id, { type: 'geojson', data })
    }

    const setLayerVisibility = (layerId: string, visible: boolean) => {
      if (!map.getLayer(layerId)) return
      map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none')
    }

    const addAqiLayer = async () => {
      try {
        const response = await api.getAQILayer()
        const aqiData = response.data?.aqi_data || []
        const geojson: GeoJSON.FeatureCollection = {
          type: 'FeatureCollection',
          features: aqiData.map((point: any) => ({
            type: 'Feature',
            properties: {
              city: point.city,
              pm25: point.pm25,
            },
            geometry: {
              type: 'Point',
              coordinates: [point.longitude, point.latitude],
            },
          })),
        }

        ensureGeoJsonSource('aqi', geojson)
        if (!map.getLayer('aqi-circles')) {
          map.addLayer({
            id: 'aqi-circles',
            type: 'circle',
            source: 'aqi',
            paint: {
              'circle-radius': 7,
              'circle-color': [
                'step',
                ['get', 'pm25'],
                '#facc15',
                100, '#fb923c',
                150, '#ef4444',
                200, '#b91c1c',
              ],
              'circle-opacity': 0.7,
              'circle-stroke-color': '#ffffff',
              'circle-stroke-width': 1,
            },
          })
        }
        setLayerVisibility('aqi-circles', activeLayers.aqi)
      } catch (error) {
        setMapError('AQI layer unavailable. Start the backend to load live data.')
      }
    }

    const addCrimeLayer = async () => {
      try {
        const response = await api.getCrimeDensity()
        const crimeData = response.data?.crime_data || []
        const geojson: GeoJSON.FeatureCollection = {
          type: 'FeatureCollection',
          features: crimeData.map((point: any) => ({
            type: 'Feature',
            properties: {
              city: point.city,
              crime_rate: point.crime_rate,
            },
            geometry: {
              type: 'Point',
              coordinates: [point.longitude, point.latitude],
            },
          })),
        }

        ensureGeoJsonSource('crime', geojson)
        if (!map.getLayer('crime-circles')) {
          map.addLayer({
            id: 'crime-circles',
            type: 'circle',
            source: 'crime',
            paint: {
              'circle-radius': 7,
              'circle-color': '#f97316',
              'circle-opacity': 0.65,
              'circle-stroke-color': '#ffffff',
              'circle-stroke-width': 1,
            },
          })
        }
        setLayerVisibility('crime-circles', activeLayers.crime)
      } catch (error) {
        setMapError('Crime layer unavailable. Start the backend to load live data.')
      }
    }

    const addWaterLayer = async () => {
      try {
        const response = await api.getWaterStress()
        const waterData = response.data?.water_data || []
        const geojson: GeoJSON.FeatureCollection = {
          type: 'FeatureCollection',
          features: waterData.map((point: any) => ({
            type: 'Feature',
            properties: {
              city: point.city,
              groundwater_depletion: point.groundwater_depletion,
            },
            geometry: {
              type: 'Point',
              coordinates: [point.longitude, point.latitude],
            },
          })),
        }

        ensureGeoJsonSource('water', geojson)
        if (!map.getLayer('water-circles')) {
          map.addLayer({
            id: 'water-circles',
            type: 'circle',
            source: 'water',
            paint: {
              'circle-radius': 7,
              'circle-color': '#3b82f6',
              'circle-opacity': 0.65,
              'circle-stroke-color': '#ffffff',
              'circle-stroke-width': 1,
            },
          })
        }
        setLayerVisibility('water-circles', activeLayers.water)
      } catch (error) {
        setMapError('Water stress layer unavailable. Start the backend to load live data.')
      }
    }

    if (activeLayers.aqi) addAqiLayer()
    else setLayerVisibility('aqi-circles', false)

    if (activeLayers.crime) addCrimeLayer()
    else setLayerVisibility('crime-circles', false)

    if (activeLayers.water) addWaterLayer()
    else setLayerVisibility('water-circles', false)
  }, [activeLayers, isMapReady])

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div variants={itemVariants} className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-primary">Map Intelligence</h1>
        <p className="text-secondary mt-2">Geo-spatial urban livability visualization and heatmap</p>
      </motion.div>

      {/* MapLibre Livability Layer */}
      <motion.div
        variants={itemVariants}
        className="bg-white rounded-lg p-6 shadow-sm border border-border"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-heading font-bold text-primary">National Livability Map</h2>
          {!isMapReady && <LoadingSpinner message="Loading map..." />}
        </div>

        {mapError && (
          <div className="mb-4 rounded-lg border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-orange-900">
            {mapError}
          </div>
        )}

        <div className="mb-4 flex flex-wrap items-center gap-3 text-xs">
          <button
            onClick={() => setActiveLayers((prev) => ({ ...prev, aqi: !prev.aqi }))}
            className={`rounded-full border px-3 py-1 transition ${
              activeLayers.aqi
                ? 'border-red-300 bg-red-50 text-red-700'
                : 'border-border text-secondary'
            }`}
          >
            AQI Layer
          </button>
          <button
            onClick={() => setActiveLayers((prev) => ({ ...prev, crime: !prev.crime }))}
            className={`rounded-full border px-3 py-1 transition ${
              activeLayers.crime
                ? 'border-orange-300 bg-orange-50 text-orange-700'
                : 'border-border text-secondary'
            }`}
          >
            Crime Layer
          </button>
          <button
            onClick={() => setActiveLayers((prev) => ({ ...prev, water: !prev.water }))}
            className={`rounded-full border px-3 py-1 transition ${
              activeLayers.water
                ? 'border-blue-300 bg-blue-50 text-blue-700'
                : 'border-border text-secondary'
            }`}
          >
            Water Layer
          </button>
        </div>

        <div
          ref={mapContainerRef}
          className="h-[600px] w-full rounded-lg border border-border"
        />

        <div className="mt-6 pt-4 border-t border-border">
          <p className="text-sm font-semibold text-primary mb-3">Livability Index</p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-500 rounded"></div>
              <span>Excellent (75+)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-500 rounded"></div>
              <span>Good (65-74)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-yellow-500 rounded"></div>
              <span>Fair (55-64)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-orange-500 rounded"></div>
              <span>Poor (45-54)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-red-500 rounded"></div>
              <span>Critical (&lt;45)</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* GIS Layers Information */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        <div className="bg-white border border-border rounded-lg p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="text-red-600" size={20} />
            </div>
            <h3 className="font-heading font-semibold text-primary">AQI Heat Layer</h3>
          </div>
          <p className="text-xs text-secondary mb-3">Real-time pollution concentration mapping</p>
          <div className="space-y-1 text-xs">
            <p>✓ PM2.5 density visualization</p>
            <p>✓ Northern pollution corridor</p>
            <p>✓ Seasonal concentration patterns</p>
          </div>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <MapPin className="text-orange-600" size={20} />
            </div>
            <h3 className="font-heading font-semibold text-primary">Crime Density Markers</h3>
          </div>
          <p className="text-xs text-secondary mb-3">Safety and crime concentration zones</p>
          <div className="space-y-1 text-xs">
            <p>✓ Crime hotspot identification</p>
            <p>✓ Women safety zones mapping</p>
            <p>✓ Urban saturation pressure</p>
          </div>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="text-blue-600" size={20} />
            </div>
            <h3 className="font-heading font-semibold text-primary">Water Stress Overlay</h3>
          </div>
          <p className="text-xs text-secondary mb-3">Groundwater & contamination zones</p>
          <div className="space-y-1 text-xs">
            <p>✓ Groundwater depletion mapping</p>
            <p>✓ Contamination risk zones</p>
            <p>✓ Water complaint density</p>
          </div>
        </div>
      </motion.div>

      {/* Map Features */}
      <motion.div
        variants={itemVariants}
        className="bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-lg p-6"
      >
        <h2 className="text-lg font-heading font-bold text-blue-900 mb-4">Interactive Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-900">
          <div>
            <p className="font-semibold mb-2">🔍 Clustering</p>
            <p className="opacity-80">Auto-cluster cities by livability tier, infrastructure resilience, and urban saturation</p>
          </div>
          <div>
            <p className="font-semibold mb-2">📍 Hover Cards</p>
            <p className="opacity-80">Real-time display of rank, score, AQI, congestion, and healthcare metrics</p>
          </div>
          <div>
            <p className="font-semibold mb-2">🎯 Click to Profile</p>
            <p className="opacity-80">Click any city marker to open detailed city profile and analysis</p>
          </div>
          <div>
            <p className="font-semibold mb-2">🗺️ Layer Toggle</p>
            <p className="opacity-80">Toggle between livability choropleth, AQI, crime density, and water stress</p>
          </div>
        </div>
      </motion.div>

      {/* Technical Stack Info */}
      <motion.div variants={itemVariants} className="text-center p-6 bg-surface rounded-lg border border-border">
        <p className="text-xs text-secondary mb-2">Phase 4: GIS & Maps (In Development)</p>
        <p className="text-sm text-primary font-medium">
          MapLibre GL JS with GeoJSON layers for livability, AQI, crime, and water overlays
        </p>
      </motion.div>
    </motion.div>
  )
}
