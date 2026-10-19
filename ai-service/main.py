import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="JanSetu AI Service",
    description="Intelligent Scheme Discovery and Citizen Assistance AI Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str # user, assistant, system
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    user_context: Optional[dict] = None # e.g. state, occupation, age

class ChatResponse(BaseModel):
    reply: str
    suggested_schemes: Optional[List[str]] = []
    action_items: Optional[List[str]] = []

class SummarizeRequest(BaseModel):
    scheme_name: str
    benefits: str
    eligibility_summary: str
    language: Optional[str] = "en"

class SummarizeResponse(BaseModel):
    summary: str
    key_takeaways: List[str]
    document_checklist: List[str]

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "jansetu-ai", "version": "1.0.0"}

@app.post("/api/ai/chat", response_model=ChatResponse)
def chat_with_advisor(request: ChatRequest):
    msg = request.message.lower()
    
    # Intelligent domain heuristic response generator
    if any(k in msg for k in ["farmer", "kisan", "crop", "land", "agriculture", "rythu"]):
        reply = (
            "Namaste! For agricultural support, you may be eligible for **PM-KISAN Samman Nidhi** "
            "(₹6,000/year income support) and the **Pradhan Mantri Fasal Bima Yojana (PMFBY)** "
            "for crop insurance. If you are in Telangana, check out **Rythu Bandhu** and the loan waiver schemes. "
            "Do you own agricultural land or livestock?"
        )
        suggested = ["PM-KISAN Samman Nidhi", "Pradhan Mantri Fasal Bima Yojana", "Rythu Bandhu"]
        actions = ["Keep Aadhaar and Land Ownership (Pattadar Passbook) ready", "Check IFSC/Bank linking with Aadhaar"]
    elif any(k in msg for k in ["student", "scholarship", "college", "study", "fee", "matric"]):
        reply = (
            "Hello! There are several scholarships tailored for your academic level. "
            "For pre-matric and post-matric studies, central scholarships like the **Post-Matric Scholarship for SC/ST/OBC** "
            "cover tuition fees and maintenance allowance. National level merit scholarships and state specific ePASS schemes "
            "also provide fee reimbursement. What is your current course and family income range?"
        )
        suggested = ["Post-Matric Scholarship Scheme", "Central Sector Scheme of Scholarships for College Students"]
        actions = ["Obtain Income Certificate (< ₹2.5 Lakhs typically)", "Keep Previous Year Marksheet handy", "Active Bank Account in Student's Name"]
    elif any(k in msg for k in ["business", "loan", "startup", "entrepreneur", "shop", "mudra"]):
        reply = (
            "Looking to start or expand a business? Under **PM Mudra Yojana (PMMY)**, collateral-free loans "
            "are available in three tiers: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakhs), and Tarun (up to ₹10 Lakhs). "
            "Additionally, the **PMEGP** scheme offers a 15% to 35% government subsidy on project costs."
        )
        suggested = ["Pradhan Mantri Mudra Yojana (PMMY)", "Prime Minister Employment Generation Programme (PMEGP)"]
        actions = ["Prepare a Project Business Report", "Collect Identity & Address proofs", "Approach nearest nationalized bank or portal"]
    elif any(k in msg for k in ["woman", "women", "girl", "mother", "maternity", "widow", "kalyana"]):
        reply = (
            "JanSetu provides dedicated discovery for women welfare initiatives: "
            "**Pradhan Mantri Matru Vandana Yojana (PMMVY)** offers maternity benefit of ₹5,000, "
            "while **Sukanya Samriddhi Yojana** offers high-interest savings for girl children. "
            "State programs like **Kalyana Lakshmi / Shaadi Mubarak** provide financial assistance for marriage."
        )
        suggested = ["PM Matru Vandana Yojana", "Sukanya Samriddhi Yojana", "Kalyana Lakshmi / Shaadi Mubarak"]
        actions = ["Aadhaar Card", "Bank Account linked to Aadhaar", "Relevant certificate (Marriage/Birth/Income)"]
    else:
        reply = (
            "Hello! I am your JanSetu AI Assistant. I can help you identify government schemes, scholarships, "
            "subsidies, and welfare programs you qualify for. You can tell me your age, occupation (farmer, student, "
            "job seeker, entrepreneur), state, or specific benefits you need."
        )
        suggested = ["Ayushman Bharat PM-JAY", "PM Awas Yojana (PMAY)", "PM Suraksha Bima Yojana"]
        actions = ["Complete your citizen profile for automated 100% accurate rule matching"]

    return ChatResponse(
        reply=reply,
        suggested_schemes=suggested,
        action_items=actions
    )

@app.post("/api/ai/summarize", response_model=SummarizeResponse)
def summarize_scheme(request: SummarizeRequest):
    return SummarizeResponse(
        summary=f"{request.scheme_name} delivers vital public assistance: {request.benefits}. Eligible citizens qualify under: {request.eligibility_summary}.",
        key_takeaways=[
            "Official direct benefit transfer (DBT) supported",
            "Verification handled through central / state public administration",
            "No agent or intermediary fees required"
        ],
        document_checklist=[
            "Aadhaar Card",
            "Proof of Residence / Domicile Certificate",
            "Bank Passbook with Aadhaar seeding",
            "Income / Caste Certificate (if applicable)"
        ]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
