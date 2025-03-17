import json
import uuid
from datetime import datetime, timedelta

# Helper function to generate ISO-formatted timestamps.
base_dt = datetime(2025, 3, 17, 14, 30)
def dt_str(offset_minutes=0):
    return (base_dt + timedelta(minutes=offset_minutes)).isoformat() + "Z"

# We'll use this value so that new CustomUser records do not conflict with your existing 3 users.
start_user_pk = 4
num_new_users = 15

# Sample Filipino names (we no longer use their pre-defined student IDs)
filipino_names = [
    "Juan Dela Cruz",
    "Maria Clara",
    "Jose Rizal",
    "Andres Bonifacio",
    "Emilio Aguinaldo",
    "Apolinario Mabini",
    "Melchora Aquino",
    "Gregoria de Jesus",
    "Gabriela Silang",
    "Antonio Luna",
    "Diego Silang",
    "Carlos P. Garcia",
    "Ramon Magsaysay",
    "Corazon Aquino",
    "Benigno Aquino III",
]

fixtures = []

# ---------- 1. CustomUser (pks start at start_user_pk) ----------
for idx, full_name in enumerate(filipino_names, start=start_user_pk):
    # Generate a student ID dynamically so it does not conflict with existing ones.
    student_id = f"C{idx:06d}"  # e.g., C000004, C000005, ...
    # For demonstration, mark one as counselor (for instance, pk == start_user_pk+2)
    is_counselor = (idx == start_user_pk + 2)
    # Similarly, designate one as ITRC staff (e.g., pk == start_user_pk+1)
    is_itrc_staff = (idx == start_user_pk + 1)
    user_obj = {
        "model": "main.customuser",
        "pk": idx,
        "fields": {
            "password": "pbkdf2_sha256$600000$dummyhashvalue$dummyhashedpassword==",
            "last_login": dt_str(0),
            "is_superuser": False,
            "username": full_name.lower().replace(" ", "."),
            "first_name": full_name.split()[0],
            "last_name": full_name.split()[-1],
            "is_staff": True,
            "is_active": True,
            "date_joined": dt_str(-5),
            "student_id": student_id,
            "full_name": full_name,
            "academic_year_level": "Senior" if idx % 3 == 0 else "Freshman",
            "contact_number": f"+63917{idx:07d}",
            "email": f"{full_name.lower().replace(' ', '.')}@example.com",
            "is_counselor": is_counselor,
            "block_reason": "",
            "block_duration": None,
            "is_itrc_staff": is_itrc_staff,
            "is_verified": True,
            "verification_status": "verified",
            "groups": [],
            "user_permissions": []
        }
    }
    fixtures.append(user_obj)

# Helper function to map an index (1..num_new_users) to a new custom user pk.
def map_user(i):
    # i from 1 to num_new_users
    return ((i - 1) % num_new_users) + start_user_pk

# ---------- 2. EmailHistory (15 records) ----------
for i in range(1, num_new_users + 1):
    eh_obj = {
        "model": "main.emailhistory",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "email": f"old_email_{i}@example.com",
            "changed_at": dt_str(10 + i)
        }
    }
    fixtures.append(eh_obj)

# ---------- 3. UserProfile (15 records) ----------
for i in range(1, num_new_users + 1):
    up_obj = {
        "model": "main.userprofile",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "avatar": None,
            "bio": f"Ito ay sample bio para kay user {i}. Mahilig sa musika at sining.",
            "is_email_verified": True,
            "new_email": None,
            "email_change_requested_at": None,
            "email_verification_requested_at": None
        }
    }
    fixtures.append(up_obj)

# ---------- 4. Feedback (15 records) ----------
feedback_texts = [
    "Maganda ang serbisyo, maraming salamat!",
    "Napakabilis ng sagot, swak para sa kabataan.",
    "Mabuting karanasan, pero sana ay may dagdag na impormasyon.",
    "Nakakatuwa ang interface ng system.",
    "Malinaw at madaling gamitin ang platform.",
    "Magaling ang pagtugon sa mga pangangailangan.",
    "Napakalinis ng design, congrats sa team!",
    "Mahusay ang customer support.",
    "Nakakainspire ang mga feature nito.",
    "Simple pero epektibo, patuloy lang!",
    "Salamat sa mabilis na pagresponde.",
    "Magandang ideya para sa mga estudyante.",
    "Ang user interface ay nakakapukaw ng interes.",
    "Nakakabigay ng pag-asa ang sistema.",
    "Talagang kapaki-pakinabang para sa kabataan."
]
for i in range(1, num_new_users + 1):
    fb_obj = {
        "model": "main.feedback",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "message": feedback_texts[(i - 1) % len(feedback_texts)],
            "sentiment_score": 20 + i,
            "is_approved": True if i % 2 == 0 else False,
            "is_excluded": False if i % 2 == 0 else True,
            "created_at": dt_str(20 + i)
        }
    }
    fixtures.append(fb_obj)

# ---------- 5. ChatMessage (15 records) ----------
chat_messages = [
    "Kamusta? Paano kita matutulungan?",
    "May problema ba sa iyong asignatura?",
    "Ano ang nararamdaman mo ngayon?",
    "Kailangan mo ba ng payo sa iyong pag-aaral?",
    "Magandang araw! Anong balita?",
    "Puwede mo bang ikwento ang iyong karanasan?",
    "Salamat sa pagbabahagi.",
    "Ano ang iyong inaasahan sa system na ito?",
    "Mayroon ka bang nais na baguhin?",
    "Huwag kang mag-alala, nandito lang kami.",
    "Ibahagi mo ang iyong nararamdaman.",
    "Kumusta ang iyong araw?",
    "Anong balita sa eskwelahan?",
    "Narito kami upang makinig.",
    "Maging positibo, kaya mo 'yan!"
]
for i in range(1, num_new_users + 1):
    cm_obj = {
        "model": "main.chatmessage",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "message": chat_messages[(i - 1) % len(chat_messages)],
            "timestamp": dt_str(40 + i),
            "is_bot_message": True if i % 3 == 0 else False,
            "message_type": "bot_message" if i % 3 == 0 else "user_message",
            "question_index": None if i % 3 == 0 else i % 10,
            "anger": 0.1 * i,
            "disgust": 0.05 * i,
            "fear": 0.02 * i,
            "happiness": 0.7,
            "sadness": 0.05,
            "surprise": 0.03,
            "neutral": 0.1,
            "anger_percentage": int(0.1 * i * 100),
            "disgust_percentage": int(0.05 * i * 100),
            "fear_percentage": int(0.02 * i * 100),
            "happiness_percentage": 70,
            "sadness_percentage": 5,
            "surprise_percentage": 3,
            "neutral_percentage": 10
        }
    }
    fixtures.append(cm_obj)

# ---------- 6. QuestionnaireProgress (15 records) ----------
for i in range(1, num_new_users + 1):
    qp_obj = {
        "model": "main.questionnaireprogress",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "last_question_index": i % 10,
            "completed": False,
            "emotion_data": {},
            "normalized_emotions": {}
        }
    }
    fixtures.append(qp_obj)

# ---------- 7. Questionnaire (15 records) ----------
questions_tagalog = [
    "Ano ang pinaka nakaka-stress sa iyong buhay akademiko?",
    "Paano mo ilalarawan ang iyong emosyon sa nakaraang buwan?",
    "Gaano ka komportable na ibahagi ang iyong nararamdaman sa pamilya?",
    "Gaano kadalas ka nakararamdam ng pagkabahala tungkol sa eskwelahan?",
    "Ilang oras ka karaniwang natutulog sa gabi?",
    "Gaano ka tiwala sa iyong kakayahan sa pag-aaral?",
    "Ano ang iyong nararamdaman kapag may pagbabago sa iyong buhay?",
    "Paano mo hinahati ang oras para sa pag-aaral at pahinga?",
    "Gaano ka motivated na tapusin ang iyong mga gawain?",
    "Alam mo ba ang mga serbisyong pangkalusugan sa inyong paaralan?"
]
for i in range(1, num_new_users + 1):
    q_obj = {
        "model": "main.questionnaire",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "question": questions_tagalog[(i - 1) % len(questions_tagalog)],
            "answer": "Sample sagot",
            "response": "Sample tugon batay sa sagot",
            "timestamp": dt_str(60 + i),
            "answer_id": str(uuid.uuid4())
        }
    }
    fixtures.append(q_obj)

# ---------- 8. Status (15 records) ----------
for i in range(1, num_new_users + 1):
    status_obj = {
        "model": "main.status",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "title": f"Status ni {filipino_names[(i - 1) % len(filipino_names)]}",
            "description": "Ito ay isang halimbawa ng status na isinulat sa wikang Filipino.",
            "plain_description": "Halimbawa ng status na plain text.",
            "emotion": "happy" if i % 2 == 0 else "sad",
            "anger": 0.1 * i,
            "disgust": 0.05 * i,
            "fear": 0.02 * i,
            "neutral": 0.1 * i,
            "happiness": 0.6 * i,
            "sadness": 0.1 * i,
            "surprise": 0.03 * i,
            "anger_percentage": int(0.1 * i * 100),
            "disgust_percentage": int(0.05 * i * 100),
            "fear_percentage": int(0.02 * i * 100),
            "neutral_percentage": int(0.1 * i * 100),
            "happiness_percentage": int(0.6 * i * 100),
            "sadness_percentage": int(0.1 * i * 100),
            "surprise_percentage": int(0.03 * i * 100),
            "created_at": dt_str(80 + i)
        }
    }
    fixtures.append(status_obj)

# ---------- 9. NotificationCounselor (15 records) ----------
# Use the designated counselor from our new users (pk = start_user_pk + 2)
counselor_pk = start_user_pk + 2
for i in range(1, num_new_users + 1):
    nc_obj = {
        "model": "main.notificationcounselor",
        "pk": i,
        "fields": {
            "user": counselor_pk,
            "message": f"{filipino_names[(i - 1) % len(filipino_names)]} ay nag-post ng bagong status.",
            "link": f"/status/{i}/",
            "is_read": False,
            "created_at": dt_str(100 + i),
            "status": i
        }
    }
    fixtures.append(nc_obj)

# ---------- 10. Notification (15 records) ----------
for i in range(1, num_new_users + 1):
    notif_obj = {
        "model": "main.notification",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "status": i,
            "reply": None,
            "notification_type": "status",
            "message": f"May bagong update sa iyong status #{i}.",
            "link": f"/status/{i}/",
            "avatar": None,
            "is_read": False,
            "created_at": dt_str(120 + i)
        }
    }
    fixtures.append(notif_obj)

# ---------- 11. ReplyNotification (15 records) ----------
for i in range(1, num_new_users + 1):
    rn_obj = {
        "model": "main.replynotification",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "status": i,
            "reply": i,  # assuming reply pk equals i
            "notification_type": "reply",
            "message": f"{filipino_names[(i - 1) % len(filipino_names)]} ay nag-reply sa iyong status.",
            "link": f"/status/{i}/",
            "avatar": None,
            "is_read": False,
            "created_at": dt_str(140 + i),
            "replied_by": ((i) % num_new_users) + start_user_pk
        }
    }
    fixtures.append(rn_obj)

# ---------- 12. UserNotificationSettings (15 records) ----------
for i in range(1, num_new_users + 1):
    uns_obj = {
        "model": "main.usernotificationsettings",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "has_clicked_notification": False
        }
    }
    fixtures.append(uns_obj)

# ---------- 13. Referral (15 records) ----------
for i in range(1, num_new_users + 1):
    ref_obj = {
        "model": "main.referral",
        "pk": i,
        "fields": {
            "status": i,
            "referred_by": map_user(i),
            "highlighted_title": f"Highlight ng Status #{i}",
            "highlighted_description": "Maikling paliwanag kung bakit inirerefer.",
            "referral_reason": "Kulang ang paliwanag",
            "other_reason": "",
            "created_at": dt_str(160 + i)
        }
    }
    fixtures.append(ref_obj)

# ---------- 14. ProfanityWord (1 record) ----------
profanities = [
    "gago", "tanga", "bobo", "ulol", "buwisit", "peste",
    "tangina", "leche", "puta", "burat", "siraulo", "tarantado",
    "yawa", "bugtong", "kalbo"
]
pw_obj = {
    "model": "main.profanityword",
    "pk": 1,
    "fields": {
        "word_list": profanities
    }
}
fixtures.append(pw_obj)

# ---------- 15. Reply (15 records) ----------
for i in range(1, num_new_users + 1):
    reply_obj = {
        "model": "main.reply",
        "pk": i,
        "fields": {
            "status": i,
            "parent_reply": None,
            "user": ((i + 2 - 1) % num_new_users) + start_user_pk,
            "text": f"Reply sample #{i} mula kay {filipino_names[(i - 1) % len(filipino_names)]}.",
            "created_at": dt_str(180 + i)
        }
    }
    fixtures.append(reply_obj)

# ---------- 16. ChatSession (15 records) ----------
for i in range(1, num_new_users + 1):
    cs_obj = {
        "model": "main.chatsession",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "counselor": counselor_pk,
            "is_active": True,
            "started_at": dt_str(200 + i),
            "ended_at": None,
            "last_message_at": dt_str(200 + i)
        }
    }
    fixtures.append(cs_obj)

# ---------- 17. CounselorMessage (15 records) ----------
for i in range(1, num_new_users + 1):
    cm_msg_obj = {
        "model": "main.counselormessage",
        "pk": i,
        "fields": {
            "chat_session": i,
            "sender": counselor_pk,
            "recipient": map_user(i),
            "message": f"Kamusta, ito ay mensahe mula sa counselor para sa session #{i}.",
            "timestamp": dt_str(220 + i)
        }
    }
    fixtures.append(cm_msg_obj)

# ---------- 18. ContactUs (15 records) ----------
for i in range(1, num_new_users + 1):
    cu_obj = {
        "model": "main.contactus",
        "pk": i,
        "fields": {
            "name": filipino_names[(i - 1) % len(filipino_names)],
            "email": f"contact{i}@example.com",
            "subject": f"Pakikipag-ugnayan #{i}",
            "message": "Ito ay mensahe para sa contact us form.",
            "created_at": dt_str(240 + i),
            "reply": "",
            "is_replied": False
        }
    }
    fixtures.append(cu_obj)

# ---------- 19. UserSession (15 records) ----------
for i in range(1, num_new_users + 1):
    us_obj = {
        "model": "main.usersession",
        "pk": i,
        "fields": {
            "user": map_user(i),
            "session_key": f"sess_{i:03d}",
            "created_at": dt_str(260 + i),
            "expire_date": (base_dt + timedelta(days=1, minutes=260 + i)).isoformat() + "Z",
            "session_end": None
        }
    }
    fixtures.append(us_obj)

# Write the fixture data to a JSON file.
with open("filipino_fixture.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, indent=2, ensure_ascii=False)

print("Fixture file 'filipino_fixture.json' has been generated with", len(fixtures), "records.")
