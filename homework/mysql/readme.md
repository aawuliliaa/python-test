# 1.准备数据
```

##年级表
DROP TABLE IF EXISTS `class_grade`;
CREATE TABLE `class_grade` (
  `gid` int NOT NULL AUTO_INCREMENT,
  `gname` varchar(32) NOT NULL,
  PRIMARY KEY (`gid`)
) ENGINE=InnoDB COMMENT='年级表' CHARSET=utf8 AUTO_INCREMENT=1;

INSERT INTO `class_grade` VALUES ('1', '一年级'), ('2', '二年级'), ('3', '三年级'), ('4', '四年级');

##班级表
##索引grade_id
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(32) NOT NULL,
  `grade_id` int NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `fk_class_grade` (`grade_id`),
  CONSTRAINT `fk_class_grade` FOREIGN KEY (`grade_id`) REFERENCES `class_grade` (`gid`)
) ENGINE=InnoDB COMMENT='班级表' CHARSET=utf8;

INSERT INTO `class` VALUES ('1', '一年一班',1), ('2', '一年二班',1),('3', '二年一班',2),('4', '三年二班',3), ('5', '四年一班',4);

##学生表
##索引class_id
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `gender` char(1) NOT NULL,
  `class_id` int(11) NOT NULL,
  `sname` varchar(32) NOT NULL, 
  PRIMARY KEY (`sid`),
  KEY `fk_class` (`class_id`),
  CONSTRAINT `fk_class` FOREIGN KEY (`class_id`) REFERENCES `class` (`cid`)
) ENGINE=InnoDB COMMENT='学生表' CHARSET=utf8;
INSERT INTO `student` VALUES ('1', '男', '1', '理解'), ('2', '女', '1', '钢蛋'), ('3', '男', '1', '张三'), ('4', '男', '1', '张一'), ('5', '女', '1', '张二'), ('6', '男', '1', '张四'), ('7', '女', '2', '铁锤'), ('8', '男', '2', '李三'), ('9', '男', '2', '李一'), ('10', '女', '2', '李二'), ('11', '男', '2', '李四'), ('12', '女', '3', '如花'), ('13', '男', '3', '刘三'), ('14', '男', '3', '刘一'), ('15', '女', '3', '刘二'), ('16', '男', '3', '刘四');

##老师表
##索引
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` varchar(32) NOT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB COMMENT='老师表' CHARSET=utf8;

INSERT INTO `teacher` VALUES ('1', '张三'), ('2', '李四'), ('3', '王五'), ('4', '朱六'), ('5', '赵七');

##课程表
##索引teacher_id
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` varchar(32) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `fk_course_teacher` (`teacher_id`),
  CONSTRAINT `fk_course_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`tid`)
) ENGINE=InnoDB COMMENT='课程表' CHARSET=utf8;


INSERT INTO `course` VALUES ('1', '生物', '2'), ('2', '物理', '1'), ('3', '体育', '3'), ('4', '美术', '1');

##成绩表
##索引student_id，course_id`
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`sid`),
  KEY `fk_score_student` (`student_id`),
  KEY `fk_score_course` (`course_id`),
  CONSTRAINT `fk_score_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`cid`),
  CONSTRAINT `fk_score_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`sid`)
) ENGINE=InnoDB COMMENT='成绩表' CHARSET=utf8;
INSERT INTO `score` VALUES ('1', '1', '1', '10'), ('2', '1', '2', '9'), ('5', '1', '4', '66'), ('6', '2', '1', '8'), ('8', '2', '3', '68'), ('9', '2', '4', '99'), ('10', '3', '1', '77'), ('11', '3', '2', '66'), ('12', '3', '3', '87'), ('13', '3', '4', '99'), ('14', '4', '1', '79'), ('15', '4', '2', '11'), ('16', '4', '3', '67'), ('17', '4', '4', '100'), ('18', '5', '1', '79'), ('19', '5', '2', '11'), ('20', '5', '3', '67'), ('21', '5', '4', '100'), ('22', '6', '1', '9'), ('23', '6', '2', '100'), ('24', '6', '3', '67'), ('25', '6', '4', '100'), ('26', '7', '1', '9'), ('27', '7', '2', '100'), ('28', '7', '3', '67'), ('29', '7', '4', '88'), ('30', '8', '1', '9'), ('31', '8', '2', '100'), ('32', '8', '3', '67'), ('33', '8', '4', '88'), ('34', '9', '1', '91'), ('35', '9', '2', '88'), ('36', '9', '3', '67'), ('37', '9', '4', '22'), ('38', '10', '1', '90'), ('39', '10', '2', '77'), ('40', '10', '3', '43'), ('41', '10', '4', '87'), ('42', '11', '1', '90'), ('43', '11', '2', '77'), ('44', '11', '3', '43'), ('45', '11', '4', '87'), ('46', '12', '1', '90'), ('47', '12', '2', '77'), ('48', '12', '3', '43'), ('49', '12', '4', '87'), ('52', '13', '3', '87');

##班级任职表
DROP TABLE IF EXISTS `teacher2cls`;
CREATE TABLE `teacher2cls` (
  `tcid` int(11) NOT NULL AUTO_INCREMENT,
  `tid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  PRIMARY KEY (`tcid`),
  KEY `fk_score_student` (`tid`),
  KEY `fk_score_course` (`cid`),
  CONSTRAINT `fk_teacher2cls_teacher` FOREIGN KEY (`tid`) REFERENCES `teacher` (`tid`),
  CONSTRAINT `fk_teacher2cls_class` FOREIGN KEY (`cid`) REFERENCES `class` (`cid`)
) ENGINE=InnoDB COMMENT='班级任职表' CHARSET=utf8;
INSERT INTO `teacher2cls` VALUES ('1', '1', '1'),('2', '1', '2'),('3', '2', '1'),('4', '3', '2');

```
# 2、查询学生总人数；
```
select count(*) from student;
```
![](.readme_images/f6130bdf.png)
# 3、查询“生物”课程和“物理”课程成绩都及格的学生id和姓名；
```

select stu.sid,stu.sname,stu_score.score from student stu -- 我这里查询出了学生的id,姓名和成绩，便于查看
inner join 
(select * from score where course_id in -- 查询出所有学生的物理和生物的成绩大于等于60的
(select cid from course where cname in('生物','物理'))-- 查询出物理和生物的cid
and score>=60 )stu_score
on stu.sid=stu_score.student_id
```
![](.readme_images/f9cdba93.png)
![](.readme_images/c1e0c9ed.png)
# 4、查询每个年级的班级数，取出班级数最多的前三个年级；
```
select gname,count(cid) count_cls  
from class cls 
inner join 
class_grade cls_gra
on cls.grade_id=cls_gra.gid  -- 查询出年级和班级的对应关系，由于我想列出年级名，所以和年级表关联一下，
                             -- 如果不想列出年级名，可直接使用班级表的grade_id分组
group by gname               -- 以谁分组，才能select哪个列(可以使用函数取其他列)，所以以gname分组
order by count_cls DESC      -- 由于order by执行顺序在sellect gname,count(cid) count_cls 之后，所以可以使用列别名
limit 3                      -- 只列出前三个年级

```
![](.readme_images/8bcdf643.png)
![](.readme_images/7c15fccd.png)
# 5、查询平均成绩最高和最低的学生的id和姓名以及平均成绩；
```
-- 查询平均成绩最高和最低的学生的id和姓名以及平均成绩；
select stu.sid,stu.sname,stu_avg_score.avg_score  -- 查询出学生id,姓名和平均成绩
from student stu 
inner join                      -- 主要是为了查询出学生姓名，才与student表关联
((select student_id,avg(score) avg_score 
from score 
group by student_id
order by avg_score desc limit 1 )-- 平均成绩最高的学生的ID和平均成绩
UNION                            -- union之后，是成绩最高和最低的两个学生信息
(select student_id,avg(score) avg_score 
from score 
group by student_id
order by avg_score asc limit 1 )) stu_avg_score -- 平均成绩最低的学生的ID和平均成绩
on stu.sid=stu_avg_score.student_id
```
![](.readme_images/d02829bc.png)
![](.readme_images/ac4a8065.png)
# 6、查询每个年级的学生人数；
```
-- 查询每个年级的学生人数；
-- 这里我使用了inner join，只列出有学生的班级，
-- 没有学生的班级count(*)后会为1，这样就有学生了
select gname,count(*) from student stu
inner join class cls
on stu.class_id=cls.cid
inner join class_grade cls_gra
on cls.grade_id=cls_gra.gid
group by gname  -- 这里按照gname分组，因为要列出gname
```
![](.readme_images/272520ee.png)
![](.readme_images/ed61a107.png)
# 7、查询每位学生的学号，姓名，选课数，平均成绩；
```
-- 查询每位学生的学号，姓名，选课数，平均成绩；
select stu.sid,stu.sname,count(sco.course_id),avg(sco.score)  -- 这里我把列名前都加了表名，
                                                              -- 明确知晓该列在哪个表中
from student stu            -- 由于要列出学生姓名，所以与student表关联
inner join score sco
on stu.sid=sco.student_id
group by stu.sid,stu.sname  -- 这里按照多个列分组，这样才能在select时，列出该列
```
![](.readme_images/c6eb679c.png)
![](.readme_images/93de4d89.png)
# 8、查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名、成绩最低的课程名及分数；
```
-- 查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名、成绩最低的课程名及分数
select sid,sname,stu_cor_sco.score,cor.cname from student  stu
inner join                   -- 与student表关联，获取学生姓名
((select student_id,course_id,score
from score 
where student_id=2 
order by score desc limit 1) -- 成绩最高的科
UNION                        -- union之后，就是该学生成绩最高和最低的信息的两条数据
(select student_id,course_id,score
from score 
where student_id=2 
order by score asc limit 1))stu_cor_sco -- 成绩最低的科
on stu.sid=stu_cor_sco.student_id
inner join course cor       -- 与course课程表关联，获取课程名
on stu_cor_sco.course_id=cor.cid
```
![](.readme_images/3f36c89e.png)
![](.readme_images/5159ef72.png)
# 9、查询姓“李”的老师的个数和所带班级数；
```
-- 查询姓“李”的老师的个数和所带班级数；
-- 我这里是算出所有李老师教的总班级数
select count(distinct tname) count_teacher ,count(cid) count_course
 from teacher tech  -- 由于需要使用老师的名字，所以使用老师表 
inner join teacher2cls t2c  -- 这张表对应着老师教授的班级

on tech.tid=t2c.tid
where tname like '李%'  -- 李老师可能教了很多个班级，所以使用count(distinct tname)找出老师数
                        -- count(cid)由于cid是不重复的，所以直接计算，可算出所有李老师教的总班级数

```
![](.readme_images/d96f37aa.png)
![](.readme_images/e38d84bd.png)
# 10、查询班级数小于5的年级id和年级名；
```
-- 查询班级数小于5的年级id和年级名
-- 查询出一个年级中，所有班级少于5个的年级id和年级名
select cls_gra.gid,cls_gra.gname,count(*)  -- 这里我把班级数也列了出来
from class cls
inner join class_grade cls_gra  -- 因为要查出年级名，所以要是用年级表
on cls.grade_id=cls_gra.gid
group by cls_gra.gid,cls_gra.gname  -- 因为要列出年级id和年级名，所以要以这两个分组
having count(*)<5                  -- 班级数少于5个，
                        -- 由于按照年级分组，每个年级中的班级是不重复的，所以使用count(*)
```
![](.readme_images/9f4c37ba.png)
![](.readme_images/83dd2dbd.png)
# 11、查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)，示例结果

![](.readme_images/1bda3346.png)
```
-- 查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)
select cls.cid,cls.caption,cls_gra.gname,
case 
when cls_gra.gid between 1 and 2 then '低年级'
when cls_gra.gid between 3 and 4 then '中年级'
when cls_gra.gid between 5 and 6 then '高年级'
end as 'grade_level'  -- 设置列别名
from class cls inner join class_grade cls_gra
on cls.grade_id=cls_gra.gid
```
![](.readme_images/4d1d85ba.png)
![](.readme_images/d7c8fe89.png)
# 12、查询学过“张三”老师2门课以上的同学的学号、姓名；
```
-- 查询学过“张三”老师2门课以上的同学的学号、姓名
select score.student_id,student.sname from score 
inner join student   -- 由于要列出学生姓名，需要与student表关联
on score.student_id=student.sid
where course_id in    -- 找出学了张三老师课的学生
(select course.cid from course inner join teacher
on course.teacher_id=teacher.tid
where teacher.tname='张三')     -- 找出张三老师教的课,cid 为2,4

group by score.student_id,student.sname -- 按照学生分组，每个学生组中的课程id是唯一的
having count(*)>=2                      -- 所以count(*)就是每个学生的课程数
                   -- 由于张三老师只教了两门课，生物和体育，所以这里就>=2才有结果
```
![](.readme_images/05d58929.png)
![](.readme_images/f9542298.png)
# 13、查询教授课程超过2门的老师的id和姓名；
```
-- 查询教授课程超过2门的老师的id和姓名
-- 表中数据只有张三老师教了两门，别的老师都只是教了一门，所以这里>=2才有结果显示，就不>2了
select teacher.tid,teacher.tname
from course inner join teacher      -- 要显示老师姓名，所以需要join teacher表
on course.teacher_id=teacher.tid
group by teacher.tid,teacher.tname   -- 由于要列出老师id和姓名，所以要把这两列加到分组中
having count(cname)>=2          -- 根据老师分组，每个老师组中的课程是唯一的，这里可以使用
                                -- count(*)或count(cid)或count(cname)
```
![](.readme_images/afcd0670.png)
![](.readme_images/4348d393.png)
# 14、查询学过编号“1”课程和编号“2”课程的同学的学号、姓名；
```
-- 查询学过编号“1”课程和编号“2”课程的同学的学号、姓名
select student.sid,student.sname
from score inner join student
on score.student_id=student.sid
where course_id in (1,2)  -- 查询counse_id为(1,2)的学生学号，姓名
group by student.sid,student.sname   -- 按照学生来分组，查询学过
having count(course_id)=2        -- 查询学过两门课程的学生，因为可能有的学生只学习过一门
```
![](.readme_images/950f13d3.png)
![](.readme_images/5344ea03.png)
# 15、查询没有带过高年级的老师id和姓名；
```
-- 查询没有带过高年级的老师id和姓名
-- grade id =5或6为高年级
select tea.tid,tea.tname
from teacher tea left  join teacher2cls t2c
on tea.tid=t2c.tid
left  join class cls
on t2c.cid=cls.cid
where grade_id is null or grade_id not in (5,6)
-- 可能有的老师没有教班级，在学校中做别的事
-- grade_id not in (5,6)会排除掉为null的值
```
![](.readme_images/20e4c7cb.png)
![](.readme_images/839285b2.png)

# 16、查询学过“张三”老师所教的所有课的同学的学号、姓名；
```

```
# 17、查询带过超过2个班级的老师的id和姓名；
```

```
# 18、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；
```

```
# 19、查询所带班级数最多的老师id和姓名；
```

```
20、查询有课程成绩小于60分的同学的学号、姓名；
```

```
21、查询没有学全所有课的同学的学号、姓名；
```

```
22、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名；
```

```
23、查询至少学过学号为“1”同学所选课程中任意一门课的其他同学学号和姓名；
```

```
24、查询和“2”号同学学习的课程完全相同的其他同学的学号和姓名；
```

```
25、删除学习“张三”老师课的score表记录；
```

```
26、向score表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“2”课程的同学学号；②插入“2”号课
程的平均成绩；
```

```
27、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 学生ID,语文,
数学,英语,课程数和平均分；
```

```
28、查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；
```

```
29、按各科平均成绩从低到高和及格率的百分数从高到低顺序；
```

```
30、课程平均分从高到低显示（现实任课老师）；
```

```
31、查询各科成绩前三名的记录(不考虑成绩并列情况) ；
32、查询每门课程被选修的学生数；
33、查询选修了2门以上课程的全部学生的学号和姓名；
34、查询男生、女生的人数，按倒序排列；
35、查询姓“张”的学生名单；
36、查询同名同姓学生名单，并统计同名人数；
37、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；
38、查询课程名称为“数学”，且分数低于60的学生姓名和分数；
39、查询课程编号为“3”且课程成绩在80分以上的学生的学号和姓名；
40、求选修了课程的学生人数
41、查询选修“王五”老师所授课程的学生中，成绩最高和最低的学生姓名及其成绩；
42、查询各个课程及相应的选修人数；
43、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；
44、查询每门课程成绩最好的前两名学生id和姓名；
45、检索至少选修两门课程的学生学号；
46、查询没有学生选修的课程的课程号和课程名；
47、查询没带过任何班级的老师id和姓名；
48、查询有两门以上课程超过80分的学生id及其平均成绩；
49、检索“3”课程分数小于60，按分数降序排列的同学学号；
50、删除编号为“2”的同学的“1”课程的成绩；
51、查询同时选修了物理课和生物课的学生id和姓名；
