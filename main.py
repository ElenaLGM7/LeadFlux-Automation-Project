from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session

import models, schemas, services, webhooks, notifications
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LeadFlux API")

app.include_router(webhooks.router)


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/lead", response_model=schemas.LeadResponse)
def create_lead(
    lead: schemas.LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    score = services.calculate_score(lead)
    status = services.classify_lead(score)

    db_lead = models.Lead(
        name=lead.name,
        email=lead.email,
        company=lead.company,
        message=lead.message,
        score=score,
        status=status
    )

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    if status == "hot":
        background_tasks.add_task(notifications.notify_lead, db_lead)

    return db_lead


@app.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()


@app.get("/leads/{status}")
def get_leads_by_status(status: str, db: Session = Depends(get_db)):
    return db.query(models.Lead).filter(models.Lead.status == status).all()
