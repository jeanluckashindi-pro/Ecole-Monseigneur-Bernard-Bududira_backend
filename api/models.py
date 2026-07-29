from django.db import models


class Inscription(models.Model):
    STATUS_CHOICES = [
        ("En attente", "En attente"),
        ("En revision", "En revision"),
        ("Acceptee", "Acceptee"),
        ("Rejetee", "Rejetee"),
    ]
    LEVEL_CHOICES = [
        ("Maternelle", "Maternelle"),
        ("ECOFO", "ECOFO"),
        ("Lycee Technique", "Lycee Technique"),
    ]
    APPLICATION_CHOICES = [
        ("Premiere inscription", "Premiere inscription"),
        ("Reinscription", "Reinscription"),
    ]
    GENDER_CHOICES = [
        ("Fille", "Fille"),
        ("Garcon", "Garcon"),
    ]
    RELATIONSHIP_CHOICES = [
        ("Pere", "Pere"),
        ("Mere", "Mere"),
        ("Tuteur", "Tuteur"),
        ("Autre responsable", "Autre responsable"),
    ]
    DOCUMENT_CHOICES = [
        ("Bulletin uniquement", "Bulletin uniquement"),
        ("Bulletin + acte de naissance", "Bulletin + acte de naissance"),
        ("Dossier complet", "Dossier complet"),
        ("Aucun pour le moment", "Aucun pour le moment"),
    ]

    application_type = models.CharField(max_length=50, choices=APPLICATION_CHOICES)
    student_status = models.CharField(max_length=50)
    school_level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    requested_class = models.CharField(max_length=100)
    previous_school = models.CharField(max_length=200, blank=True, default="")
    guardian_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, default="")
    address = models.TextField()
    school_year = models.CharField(max_length=20)
    documents = models.CharField(max_length=100, choices=DOCUMENT_CHOICES, default="Bulletin uniquement")
    message = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="En attente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'col"."inscription'
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name} - {self.school_level}"


class Student(models.Model):
    LEVEL_CHOICES = [
        ("Maternelle", "Maternelle"),
        ("ECOFO", "ECOFO"),
        ("Lycee Technique", "Lycee Technique"),
    ]
    GENDER_CHOICES = [
        ("Fille", "Fille"),
        ("Garcon", "Garcon"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    school_level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    current_class = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, default="")
    address = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'col"."student'
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    STATUS_CHOICES = [
        ("Actif", "Actif"),
        ("En conge", "En conge"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'col"."teacher'
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Message(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, default="")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'col"."message'
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("inscription", "Inscription"),
        ("inscription_accepted", "Inscription acceptee"),
        ("inscription_rejected", "Inscription rejetee"),
        ("message", "Message"),
        ("teacher_added", "Enseignant ajoute"),
        ("system", "Systeme"),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'col"."activity_log'
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.action}] {self.description[:50]}"


class Media(models.Model):
    image = models.ImageField(upload_to="images/")
    alt_text = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'col"."media'
        ordering = ["-created_at"]

    def __str__(self):
        return self.image.name


class SchoolConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'col"."school_config'

    def __str__(self):
        return self.key
