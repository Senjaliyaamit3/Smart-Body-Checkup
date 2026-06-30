import os
import joblib
import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Prediction

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ================= BASE PATH =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ================= LOAD MODELS =================
diabetes_model = joblib.load(os.path.join(BASE_DIR, "ml_models", "diabetes.pkl"))
heart_model    = joblib.load(os.path.join(BASE_DIR, "ml_models", "heart.pkl"))
kidney_model   = joblib.load(os.path.join(BASE_DIR, "ml_models", "kidney.pkl"))


# ================= SAFE CONVERTER =================
def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


# ================= PREDICTION VIEW =================
@login_required
def prediction(request):

    result      = None
    probability = None

    if request.method == "POST":

        disease = request.POST.get("disease")

        # ---- DIABETES ----
        if disease == "diabetes":
            data = np.array([[
                safe_float(request.POST.get("Pregnancies")),
                safe_float(request.POST.get("Glucose")),
                safe_float(request.POST.get("BloodPressure")),
                safe_float(request.POST.get("SkinThickness")),
                safe_float(request.POST.get("Insulin")),
                safe_float(request.POST.get("BMI")),
                safe_float(request.POST.get("DiabetesPedigreeFunction")),
                safe_float(request.POST.get("Age")),
            ]])
            pred = diabetes_model.predict(data)[0]
            probability = round(diabetes_model.predict_proba(data)[0][pred] * 100, 2) if hasattr(diabetes_model, "predict_proba") else 0
            result = "Positive" if pred == 1 else "Negative"

        # ---- HEART ----
        elif disease == "heart":
            data = np.array([[
                safe_float(request.POST.get("age")),
                safe_float(request.POST.get("sex")),
                safe_float(request.POST.get("cp")),
                safe_float(request.POST.get("trestbps")),
                safe_float(request.POST.get("chol")),
                safe_float(request.POST.get("fbs")),
                safe_float(request.POST.get("restecg")),
                safe_float(request.POST.get("thalach")),
                safe_float(request.POST.get("exang")),
                safe_float(request.POST.get("oldpeak")),
                safe_float(request.POST.get("slope")),
                safe_float(request.POST.get("ca")),
                safe_float(request.POST.get("thal")),
            ]])
            pred = heart_model.predict(data)[0]
            probability = round(heart_model.predict_proba(data)[0][pred] * 100, 2) if hasattr(heart_model, "predict_proba") else 0
            result = "Positive" if pred == 1 else "Negative"

        # ---- KIDNEY ----
        elif disease == "kidney":
            data = np.array([[
                safe_float(request.POST.get("age")),
                safe_float(request.POST.get("bp")),
                safe_float(request.POST.get("sg")),
                safe_float(request.POST.get("al")),
                safe_float(request.POST.get("su")),
                safe_float(request.POST.get("rbc")),
                safe_float(request.POST.get("pc")),
                safe_float(request.POST.get("pcc")),
                safe_float(request.POST.get("ba")),
                safe_float(request.POST.get("bgr")),
                safe_float(request.POST.get("bu")),
                safe_float(request.POST.get("sc")),
                safe_float(request.POST.get("sod")),
                safe_float(request.POST.get("pot")),
                safe_float(request.POST.get("hemo")),
                safe_float(request.POST.get("pcv")),
                safe_float(request.POST.get("wc")),
                safe_float(request.POST.get("rc")),
                safe_float(request.POST.get("htn")),
                safe_float(request.POST.get("dm")),
                safe_float(request.POST.get("cad")),
                safe_float(request.POST.get("appet")),
                safe_float(request.POST.get("pe")),
                safe_float(request.POST.get("ane")),
            ]])
            pred = kidney_model.predict(data)[0]
            probability = round(kidney_model.predict_proba(data)[0][pred] * 100, 2) if hasattr(kidney_model, "predict_proba") else 0
            result = "Positive" if pred == 1 else "Negative"

        # ---- SAVE ----
        Prediction.objects.create(
            user=request.user,
            disease=disease.title(),
            result=result,
            probability=probability
        )

        # ---- EMAIL ----
        try:
            send_mail(
                subject=f"Health Prediction Result - {request.user.username}",
                message=f"""
Health Prediction Result
===================================
Username   : {request.user.username}
Disease    : {disease.title()}
Result     : {result}
Probability: {probability}%
===================================
Smart Body Checkup website.
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception as e:
            print("EMAIL ERROR:", e)

    history = Prediction.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "prediction.html", {
        "result": result,
        "probability": probability,
        "history": history,
    })


# ================= PDF REPORT VIEW =================
@login_required
def download_report(request, pk):
    pred = Prediction.objects.get(pk=pk, user=request.user)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="HealthReport_{pred.disease}_{pred.pk}.pdf"'

    doc    = SimpleDocTemplate(response, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    story  = []

    # ---- Header ----
    title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=22,
                                 textColor=colors.HexColor("#1a73e8"), spaceAfter=4, alignment=TA_CENTER)
    sub_style   = ParagraphStyle("sub", parent=styles["Normal"], fontSize=11,
                                 textColor=colors.grey, alignment=TA_CENTER, spaceAfter=2)

    story.append(Paragraph("Smart Body Checkup", title_style))
    story.append(Paragraph("AI-Powered Health Prediction Report", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a73e8"), spaceAfter=16))

    # ---- Patient Info ----
    info_style = ParagraphStyle("info", parent=styles["Normal"], fontSize=11, leading=18)
    story.append(Paragraph("<b>Patient Information</b>", ParagraphStyle("h", parent=styles["Heading2"],
                           textColor=colors.HexColor("#1a73e8"), spaceAfter=6)))

    patient_data = [
        ["Username",  request.user.username],
        ["Full Name", f"{request.user.first_name} {request.user.last_name}".strip() or "N/A"],
        ["Email",     request.user.email or "N/A"],
    ]
    # attach Patient profile fields if available
    try:
        p = request.user.patient
        patient_data += [
            ["Age",        str(p.age)],
            ["Gender",     p.gender],
            ["Phone",      p.phone],
            ["Blood Group",p.blood_group],
            ["Height",     f"{p.height} cm"],
            ["Weight",     f"{p.weight} kg"],
        ]
    except Exception:
        pass

    t = Table(patient_data, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (0, -1), colors.HexColor("#e8f0fe")),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#dadce0")),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 18))

    # ---- Prediction Result ----
    story.append(Paragraph("<b>Prediction Result</b>", ParagraphStyle("h", parent=styles["Heading2"],
                           textColor=colors.HexColor("#1a73e8"), spaceAfter=6)))

    result_color = colors.HexColor("#d93025") if pred.result == "Positive" else colors.HexColor("#188038")
    risk_label   = "HIGH RISK" if pred.result == "Positive" else "LOW RISK"

    result_data = [
        ["Disease",     pred.disease],
        ["Prediction",  pred.result],
        ["Confidence",  f"{pred.probability}%"],
        ["Risk Level",  risk_label],
        ["Date & Time", pred.created_at.strftime("%d %B %Y, %H:%M")],
    ]

    tr = Table(result_data, colWidths=[5*cm, 11*cm])
    tr.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (0, -1), colors.HexColor("#e8f0fe")),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#dadce0")),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",   (1, 1), (1, 1), result_color),
        ("TEXTCOLOR",   (1, 3), (1, 3), result_color),
        ("FONTNAME",    (1, 1), (1, 1), "Helvetica-Bold"),
    ]))
    story.append(tr)
    story.append(Spacer(1, 18))

    # ---- Recommendation ----
    story.append(Paragraph("<b>Health Recommendations</b>", ParagraphStyle("h", parent=styles["Heading2"],
                           textColor=colors.HexColor("#1a73e8"), spaceAfter=6)))

    if pred.result == "Positive":
        rec = (
            "The AI model indicates a <b>higher risk</b> for this condition. "
            "Please consult a qualified doctor immediately for further medical evaluation. "
            "Do not rely solely on this report for diagnosis or treatment decisions."
        )
    else:
        rec = (
            "No significant risk detected. Maintain a healthy lifestyle — eat a balanced diet, "
            "exercise for at least 30 minutes daily, sleep 7–8 hours per night, "
            "and visit your doctor for regular checkups."
        )

    story.append(Paragraph(rec, ParagraphStyle("rec", parent=styles["Normal"], fontSize=10,
                           leading=16, textColor=colors.HexColor("#3c4043"))))
    story.append(Spacer(1, 18))

    # ---- Disclaimer ----
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dadce0"), spaceAfter=8))
    story.append(Paragraph(
        "<i>Disclaimer: This report is generated by an AI model and is for informational purposes only. "
        "It is not a substitute for professional medical advice, diagnosis, or treatment.</i>",
        ParagraphStyle("disc", parent=styles["Normal"], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(story)
    return response