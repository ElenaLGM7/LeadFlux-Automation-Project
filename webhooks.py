from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
import models, services, notifications
from database import get_db

router = APIRouter(prefix="/webhook", tags=["Webhooks"])


@router.post("/lead")
async def receive_lead(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    data = await request.json()

    name = data.get("name")
    email = data.get("email")
    company = data.get("company")
    message = data.get("message")

    lead_obj = type("LeadObj", (), {
        "name": name,
        "email": email,
        "company": company,
        "message": message
    })

    score = services.calculate_score(lead_obj)
    status = services.classify_lead(score)

    db_lead = models.Lead(
        name=name,
        email=email,
        company=company,
        message=message,
        score=score,
        status=status
    )

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    if status == "hot":
        background_tasks.add_task(notifications.notify_lead, db_lead)

    return {"status": "received", "id": db_lead.id}
