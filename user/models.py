from django.db import models
from django.contrib.auth.models import User


# # Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    idcard = models.BigIntegerField(db_column="idcard", verbose_name="身份证")
    photo = models.ImageField(upload_to="user", null=True)  # 头像


class Recruitment(models.Model):
    RECORD_CHOICE = [('L', '学历不限'), ('M', '中专及以上学历'), ('D', '大专及以上学历'), ('C', '本科及以上学历')]
    EXPERIENCE_CHOICE = [('L', '经验不限'), ('H', '有类似工作经验')]
    title = models.CharField(max_length=100, db_column="title", verbose_name="招聘标题")
    low_remuneration = models.IntegerField(db_column='low_remuneration', verbose_name="最低报酬")
    high_remuneration = models.IntegerField(db_column='high_remuneration', verbose_name="最高报酬")
    recruit_num = models.IntegerField(db_column="recruit_num", verbose_name="招收人数")
    experience = models.CharField(max_length=32, db_column="experience", verbose_name="经验要求", choices=EXPERIENCE_CHOICE)
    record_schooling = models.CharField(max_length=32, db_column="record_schooling", verbose_name="学历要求",
                                        choices=RECORD_CHOICE)
    position_describe = models.TextField(max_length=3000, db_column="position_describe", verbose_name="岗位职责")
    job_specification = models.TextField(max_length=3000, db_column="specification", verbose_name="任职要求")
    salary_specification = models.TextField(max_length=2000, db_column="salary_specification", verbose_name="工资薪资")
    welfare_treatment = models.TextField(max_length=2000, db_column="welfare_treatment", verbose_name="福利待遇")
    contact_phone = models.CharField(max_length=12, db_column='contact_phone', verbose_name="联系方式")

    class Meta:
        db_table = "recruitment"
