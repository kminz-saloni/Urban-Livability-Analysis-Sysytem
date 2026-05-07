from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO, StringIO
import csv
from database import get_db
from services.data_processing import get_data_service
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = APIRouter()


def _build_pdf(title: str, lines: list[str]) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, height - 60, title)

    pdf.setFont("Helvetica", 10)
    y = height - 90
    for line in lines:
        if y < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 60
        pdf.drawString(40, y, line)
        y -= 16

    pdf.save()
    buffer.seek(0)
    return buffer


@router.get("/summary")
async def get_report_summary(db: Session = Depends(get_db)):
    service = get_data_service()
    results = service.get_full_pipeline_results()
    payload = service.get_report_payload()
    payload["insights"] = results["insights"]
    return payload


@router.get("/rankings.csv")
async def download_rankings_csv(db: Session = Depends(get_db)):
    service = get_data_service()
    results = service.get_full_pipeline_results()
    rankings = results["rankings"]

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=rankings[0].keys())
    writer.writeheader()
    writer.writerows(rankings)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=city-rankings.csv"},
    )


@router.get("/national.pdf")
async def download_national_report(db: Session = Depends(get_db)):
    service = get_data_service()
    payload = service.get_report_payload()

    lines = [
        f"Total cities: {payload['summary']['cities']}",
        f"Average score: {payload['summary']['avg_score']:.2f}",
        f"Top city: {payload['summary']['top_city']}",
        f"Bottom city: {payload['summary']['bottom_city']}",
        "",
        "Top 5 Cities:",
    ]

    for city in payload["top_10"][:5]:
        lines.append(f"- {city['city_name']} ({city['livability_score']:.1f})")

    lines.append("")
    lines.append("Bottom 5 Cities:")
    for city in payload["bottom_10"][:5]:
        lines.append(f"- {city['city_name']} ({city['livability_score']:.1f})")

    buffer = _build_pdf("UrbanPulse IQ - National Livability Report", lines)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=national-livability-report.pdf"},
    )


@router.get("/compare.pdf")
async def download_comparison_report(
    cities: str = Query("", description="Comma-separated list of cities"),
    db: Session = Depends(get_db),
):
    service = get_data_service()
    results = service.get_full_pipeline_results()
    rankings = results["rankings"]

    requested = [city.strip() for city in cities.split(",") if city.strip()]
    if not requested:
        requested = [r["city_name"] for r in rankings[:3]]

    selected = [r for r in rankings if r["city_name"] in requested]

    lines = ["Selected cities:"]
    for city in selected:
        lines.append(
            f"- {city['city_name']} | Score: {city['livability_score']:.1f} | Rank: {city['rank']}"
        )

    buffer = _build_pdf("UrbanPulse IQ - City Comparison Report", lines)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=city-comparison-report.pdf"},
    )
