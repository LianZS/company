import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User


# # Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    idcard = models.BigIntegerField(db_column="idcard", verbose_name="身份证")
    photo = models.ImageField(upload_to="user", null=True)  # 头像


class Recruitment(models.Model):
    """
    招聘信息表
    """
    RECORD_CHOICE = [('L', '学历不限'), ('M', '中专及以上学历'), ('D', '大专及以上学历'), ('C', '本科及以上学历')]
    EXPERIENCE_CHOICE = [('L', '经验不限'), ('H', '有类似工作经验')]
    GENDER_CHOICE = [('M', '男'), ('L', '女')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, db_column="title", verbose_name="招聘标题")
    low_remuneration = models.IntegerField(db_column='low_remuneration', verbose_name="最低报酬")
    high_remuneration = models.IntegerField(db_column='high_remuneration', verbose_name="最高报酬")
    recruit_num = models.IntegerField(db_column="recruit_num", verbose_name="招收人数")
    gender = models.CharField(max_length=4, db_column="gender", choices=GENDER_CHOICE, verbose_name="性别要求")
    experience = models.CharField(max_length=32, db_column="experience", verbose_name="经验要求", choices=EXPERIENCE_CHOICE)
    record_schooling = models.CharField(max_length=32, db_column="record_schooling", verbose_name="学历要求",
                                        choices=RECORD_CHOICE)
    position_describe = models.TextField(max_length=3000, db_column="position_describe", verbose_name="岗位职责")
    job_specification = models.TextField(max_length=3000, db_column="specification", verbose_name="任职要求")
    salary_specification = models.TextField(max_length=2000, db_column="salary_specification", verbose_name="工资薪资")
    welfare_treatment = models.TextField(max_length=2000, db_column="welfare_treatment", verbose_name="福利待遇")
    contact_phone = models.CharField(max_length=11, db_column='contact_phone', verbose_name="联系方式")
    work_address = models.CharField(max_length=32, db_column="address", verbose_name="公众地点")
    release_time = models.DateField(db_column="release_time", default=datetime.datetime.now().date(),
                                    verbose_name="发布时间")
    create_time = models.DateTimeField(db_column="create_time", verbose_name="数据创建时间", default=datetime.datetime.now())

    class Meta:
        db_table = "recruitment"


class ApplicantModel(models.Model):
    GENDER_CHOICE = [('M', '男'), ('L', '女')]
    RECORD_CHOICE = [('A', '小学'), ('B', '初中'), ('C', '中专'), ('D', '大专'), ('E', "本科"), ('F', "研究生")]

    uid = models.OneToOneField(Recruitment, to_field="id", on_delete=models.CASCADE)
    name = models.CharField(max_length=16, db_column="name", verbose_name="姓名")
    gender = models.CharField(max_length=2, db_column="gender", choices=GENDER_CHOICE, verbose_name="性别")
    age = models.SmallIntegerField(db_column="age", verbose_name="年龄")
    record_schooling = models.CharField(max_length=1, db_column="record_schooling", choices=RECORD_CHOICE,
                                        verbose_name="学历")
    contact_phone = models.CharField(max_length=11, db_column='contact_phone', verbose_name="联系方式")
    native_place = models.CharField(max_length=32, db_column="native_place", verbose_name="籍贯")
    experience = models.TextField(max_length=360, db_column="experience", verbose_name="工作经验")
    talent = models.TextField(max_length=360, db_column="talent", verbose_name="特长", null=True)

    class Meta:
        db_table = "application"
