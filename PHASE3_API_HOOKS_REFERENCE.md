# Phase 3 API & Hooks Quick Reference

## Custom React Hooks Reference

### Ranking Hooks

#### `useRankings(limit?: number)`
Fetch all city rankings with optional limit.
```typescript
const { data, loading, error } = useRankings()
// data: City[]
```

#### `useTopCities(limit: number = 10)`
Fetch top N cities.
```typescript
const { data: cities, loading, error } = useTopCities(10)
// data: City[] (sorted by score descending)
```

#### `useBottomCities(limit: number = 10)`
Fetch bottom N cities.
```typescript
const { data: cities, loading, error } = useBottomCities(10)
// data: City[] (sorted by score ascending)
```

#### `useRankingStats()`
Fetch statistics (mean, median, std-dev, min, max).
```typescript
const { data: stats, loading, error } = useRankingStats()
// stats: {
//   mean_score: number
//   median_score: number
//   std_dev: number
//   min_score: number
//   max_score: number
// }
```

#### `useCityProfile(cityName?: string)`
Fetch detailed single city profile.
```typescript
const { data: city, loading, error } = useCityProfile('Bangalore')
// city: City | null
```

#### `useCitiesByTier(tier: string)`
Filter cities by tier (Tier-1, Tier-2, Tier-3).
```typescript
const { data: cities, loading, error } = useCitiesByTier('Tier-1')
// data: City[]
```

#### `useStressIndicators()`
Compute tier statistics and stress levels.
```typescript
const { tiers, loading, error } = useStressIndicators()
// tiers: TierStats[] = [
//   { tier: 'Tier-1', count: 3, avgScore: 62.45, stressLevel: 'high' },
//   ...
// ]
```

### Analytics Hooks

#### `useInsights()`
Fetch AI-generated insights.
```typescript
const { insights, loading, error } = useInsights()
// insights: Insight[] = [
//   { title: string, description: string, type: 'positive'|'warning'|'critical', confidence: number },
//   ...
// ]
```

#### `useAQIAnalytics()`
Fetch AQI and pollution analytics.
```typescript
const { data, loading, error } = useAQIAnalytics()
```

#### `useCrimeAnalytics()`
Fetch crime data.
```typescript
const { data, loading, error } = useCrimeAnalytics()
```

#### `useWaterAnalytics()`
Fetch water stress data.
```typescript
const { data, loading, error } = useWaterAnalytics()
```

#### `useTrafficAnalytics()`
Fetch traffic and congestion data.
```typescript
const { data, loading, error } = useTrafficAnalytics()
```

## API Endpoints Reference

### Ranking Endpoints

#### `GET /api/rankings`
Get all city rankings.
```bash
curl http://localhost:8000/api/rankings?limit=10
```

#### `GET /api/rankings/top`
Get top N cities.
```bash
curl http://localhost:8000/api/rankings/top?limit=10
```

#### `GET /api/rankings/bottom`
Get bottom N cities.
```bash
curl http://localhost:8000/api/rankings/bottom?limit=10
```

#### `GET /api/rankings/stats`
Get statistics.
```bash
curl http://localhost:8000/api/rankings/stats
```
Response:
```json
{
  "mean_score": 64.88,
  "median_score": 69.54,
  "std_dev": 13.47,
  "min_score": 49.12,
  "max_score": 78.50
}
```

#### `GET /api/rankings/insights`
Get AI-generated insights.
```bash
curl http://localhost:8000/api/rankings/insights
```
Response:
```json
{
  "insights": [
    {
      "title": "Tier-2 City Outperformance",
      "description": "...",
      "type": "positive",
      "confidence": 0.85
    }
  ]
}
```

#### `GET /api/rankings/{city_name}`
Get single city profile.
```bash
curl http://localhost:8000/api/rankings/Bangalore
```

#### `GET /api/rankings/by-tier/{tier}`
Get cities by tier.
```bash
curl http://localhost:8000/api/rankings/by-tier/Tier-1
```

### Analytics Endpoints

#### `GET /api/analytics/aqi`
Get AQI analytics.
```bash
curl http://localhost:8000/api/analytics/aqi
```

#### `GET /api/analytics/crime`
Get crime analytics.
```bash
curl http://localhost:8000/api/analytics/crime
```

#### `GET /api/analytics/water`
Get water analytics.
```bash
curl http://localhost:8000/api/analytics/water
```

#### `GET /api/analytics/traffic`
Get traffic analytics.
```bash
curl http://localhost:8000/api/analytics/traffic
```

## Usage Examples

### Dashboard Page
```typescript
'use client'
import { useTopCities, useRankingStats, useInsights, useStressIndicators } from '@/hooks/useData'

export default function Dashboard() {
  const { data: topCities, loading: citiesLoading } = useTopCities(10)
  const { data: stats, loading: statsLoading } = useRankingStats()
  const { insights, loading: insightsLoading } = useInsights()
  const { tiers, loading: tiersLoading } = useStressIndicators()

  if (citiesLoading || statsLoading || insightsLoading || tiersLoading) {
    return <LoadingSpinner />
  }

  return (
    <div>
      <KPICard label="Avg Score" value={stats?.mean_score.toFixed(1)} />
      <CityRankingChart cities={topCities} />
      <UrbanStressIndicators tiers={tiers} />
      <InsightsPanel insights={insights} />
    </div>
  )
}
```

### Analytics Page
```typescript
import { useAQIAnalytics, useCrimeAnalytics, useWaterAnalytics, useTrafficAnalytics } from '@/hooks/useData'

export default function Analytics() {
  const { data: aqiData } = useAQIAnalytics()
  const { data: crimeData } = useCrimeAnalytics()
  const { data: waterData } = useWaterAnalytics()
  const { data: trafficData } = useTrafficAnalytics()

  return (
    <div className="space-y-6">
      <Tab title="AQI" content={renderAQIChart(aqiData)} />
      <Tab title="Crime" content={renderCrimeChart(crimeData)} />
      <Tab title="Water" content={renderWaterChart(waterData)} />
      <Tab title="Traffic" content={renderTrafficChart(trafficData)} />
    </div>
  )
}
```

### Comparison Page
```typescript
import { useCityProfile } from '@/hooks/useData'

export default function Comparison() {
  const { data: city1 } = useCityProfile('Bangalore')
  const { data: city2 } = useCityProfile('Mumbai')

  return (
    <div>
      <RadarChart cities={[city1, city2]} />
      <CategoryBreakdown cities={[city1, city2]} />
    </div>
  )
}
```

## TypeScript Interfaces

### City Interface
```typescript
interface City {
  rank: number
  city_name: string
  state: string
  livability_score: number
  percentile: number
  tier: string
  category_scores?: Record<string, number>
  raw_metrics?: Record<string, number>
}
```

### RankingStats Interface
```typescript
interface RankingStats {
  mean_score: number
  median_score: number
  std_dev: number
  min_score: number
  max_score: number
}
```

### Insight Interface
```typescript
interface Insight {
  title: string
  description: string
  type: string
  confidence: number
}
```

### TierStats Interface
```typescript
interface TierStats {
  tier: string
  count: number
  avgScore: number
  stressLevel: 'low' | 'medium' | 'high'
}
```

## Common Patterns

### Loading State Management
```typescript
const { data, loading, error } = useRankingStats()

if (loading) return <LoadingSpinner />
if (error) return <ErrorMessage error={error} />
return <Component data={data} />
```

### Multiple Hooks
```typescript
const hook1 = useTopCities(10)
const hook2 = useRankingStats()
const hook3 = useInsights()

const isLoading = hook1.loading || hook2.loading || hook3.loading
```

### Error Handling
```typescript
const { data, error } = useCityProfile(cityName)

if (error) {
  return (
    <div className="text-red-600">
      Failed to load city: {error}
    </div>
  )
}
```

## Testing Commands

### Start Backend
```bash
cd backend
uvicorn main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Start Frontend
```bash
cd frontend
npm run dev
# Frontend available at http://localhost:3000
```

### Test APIs with curl
```bash
# Get all rankings
curl http://localhost:8000/api/rankings

# Get top 10 cities
curl http://localhost:8000/api/rankings/top?limit=10

# Get statistics
curl http://localhost:8000/api/rankings/stats

# Get single city
curl http://localhost:8000/api/rankings/Bangalore

# Get insights
curl http://localhost:8000/api/rankings/insights
```

## Performance Tips

1. **Memoize hooks in components**: Use `useMemo` to prevent unnecessary recalculations
2. **Batch requests**: Load related data together when possible
3. **Cache results**: Consider adding caching layer for frequently accessed data
4. **Pagination**: Use limit parameter to reduce payload size
5. **Error boundaries**: Wrap components with error boundaries for better error handling

## Future Enhancements

- [ ] Add pagination support to hooks
- [ ] Implement caching strategy
- [ ] Add retry logic for failed requests
- [ ] Add request cancellation for component unmount
- [ ] Add optimistic updates
- [ ] Implement real-time data updates with WebSockets
- [ ] Add data transformation/filtering in hooks
