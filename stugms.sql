--
-- SQLiteStudio v3.4.18 生成的文件，周二 10月 6 19:33:03 2026
--
-- 所用的文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：tb_class
DROP TABLE IF EXISTS tb_class;

CREATE TABLE IF NOT EXISTS tb_class (
    classID   INTEGER    NOT NULL
                         UNIQUE,
    className TEXT (200) PRIMARY KEY
                         UNIQUE
);

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         1,
                         '一班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         2,
                         '二班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         3,
                         '三班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         4,
                         '四班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         5,
                         '五班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         6,
                         '六班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         7,
                         '七班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         8,
                         '八班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         9,
                         '九班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         10,
                         '十班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         11,
                         '十一班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         12,
                         '十二班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         13,
                         'AA班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         14,
                         'AAC班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         15,
                         'AB班'
                     );

INSERT INTO tb_class (
                         classID,
                         className
                     )
                     VALUES (
                         16,
                         'ACS班'
                     );


-- 表：tb_department
DROP TABLE IF EXISTS tb_department;

CREATE TABLE IF NOT EXISTS tb_department (
    dapartmentID   TEXT (200) UNIQUE,
    departmentName TEXT (200) PRIMARY KEY
                              UNIQUE
);

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202601',
                              '信息工程学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202602',
                              '文法学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202608',
                              '生物工程学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202607',
                              '机电工程学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202606',
                              '经济与管理学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202605',
                              '食品工程学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202604',
                              '外国语学院'
                          );

INSERT INTO tb_department (
                              dapartmentID,
                              departmentName
                          )
                          VALUES (
                              'A202603',
                              '艺术学院'
                          );


-- 表：tb_examkinds
DROP TABLE IF EXISTS tb_examkinds;

CREATE TABLE IF NOT EXISTS tb_examkinds (
    kindID   INTEGER NOT NULL
                     PRIMARY KEY AUTOINCREMENT,
    kindName TEXT    NOT NULL
);

INSERT INTO tb_examkinds (
                             kindID,
                             kindName
                         )
                         VALUES (
                             1,
                             '期中考试'
                         );

INSERT INTO tb_examkinds (
                             kindID,
                             kindName
                         )
                         VALUES (
                             2,
                             '期末考试'
                         );

INSERT INTO tb_examkinds (
                             kindID,
                             kindName
                         )
                         VALUES (
                             3,
                             '平时测试'
                         );

INSERT INTO tb_examkinds (
                             kindID,
                             kindName
                         )
                         VALUES (
                             4,
                             '112测试'
                         );

INSERT INTO tb_examkinds (
                             kindID,
                             kindName
                         )
                         VALUES (
                             5,
                             '22测试'
                         );


-- 表：tb_grade
DROP TABLE IF EXISTS tb_grade;

CREATE TABLE IF NOT EXISTS tb_grade (
    gradeID   INTEGER NOT NULL
                      UNIQUE,
    gradeName TEXT    PRIMARY KEY
                      UNIQUE
);

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         1,
                         '大一'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         2,
                         '大二'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         3,
                         '大三'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         4,
                         '大四'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         5,
                         '高一'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         6,
                         '高二'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         7,
                         '高三'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         8,
                         'AA'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         9,
                         'ASD'
                     );

INSERT INTO tb_grade (
                         gradeID,
                         gradeName
                     )
                     VALUES (
                         10,
                         'AW'
                     );


-- 表：tb_major
DROP TABLE IF EXISTS tb_major;

CREATE TABLE IF NOT EXISTS tb_major (
    majorID      TEXT (200) UNIQUE,
    majorName    TEXT (200) PRIMARY KEY
                            UNIQUE,
    departmentID TEXT (200) REFERENCES tb_department (dapartmentID) 
);

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M001',
                         '计算机科学与技术',
                         'A202601'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M002',
                         '信息工程',
                         'A202601'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M003',
                         '通信工程',
                         'A202601'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M004',
                         '信息与计算科学',
                         'A202601'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M006',
                         '汉语言文学',
                         'A202602'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M005',
                         '人工智能',
                         'A202601'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M011',
                         '服装与服饰设计',
                         'A202603'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M010',
                         '环境设计',
                         'A202603'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M009',
                         '法学',
                         'A202602'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M008',
                         '新闻学',
                         'A202602'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M007',
                         '汉语国际教育',
                         'A202602'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M014',
                         '工艺美术',
                         'A202603'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M013',
                         '产品设计',
                         'A202603'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M012',
                         '视觉传达设计',
                         'A202603'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M017',
                         '翻译',
                         'A202604'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M016',
                         '商务英语',
                         'A202604'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M015',
                         '英语',
                         'A202604'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M022',
                         '食品营养与健康',
                         'A202605'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M021',
                         '酒店管理',
                         'A202605'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M020',
                         '旅游管理',
                         'A202605'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M019',
                         '食品质量与安全',
                         'A202605'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M018',
                         '食品科学与工程',
                         'A202605'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M027',
                         '物流管理',
                         'A202606'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M026',
                         '信息管理与信息系统',
                         'A202606'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M025',
                         '人力资源管理',
                         'A202606'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M024',
                         '市场营销',
                         'A202606'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M023',
                         '国际经济与贸易',
                         'A202606'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M032',
                         '机械设计制造及其自动化',
                         'A202607'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M031',
                         '电气工程及其自动化',
                         'A202607'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M030',
                         '电子信息工程',
                         'A202607'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M029',
                         '机械电子工程',
                         'A202607'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M028',
                         '测控仪器与技术',
                         'A202607'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M038',
                         '环境科学',
                         'A202608'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M037',
                         '城乡规划',
                         'A202608'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M036',
                         '园林',
                         'A202608'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M035',
                         '化学工程与工艺',
                         'A202608'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M034',
                         '生物技术',
                         'A202608'
                     );

INSERT INTO tb_major (
                         majorID,
                         majorName,
                         departmentID
                     )
                     VALUES (
                         'M033',
                         '生物工程',
                         'A202608'
                     );


-- 表：tb_result
DROP TABLE IF EXISTS tb_result;

CREATE TABLE IF NOT EXISTS tb_result (
    stuID          TEXT       PRIMARY KEY,
    stuName        TEXT (200),
    gradeName      TEXT (200) REFERENCES tb_grade (gradeName),
    className      TEXT (200) REFERENCES tb_class (className),
    departmentName TEXT (200) REFERENCES tb_department (departmentName),
    majorName      TEXT (200) REFERENCES tb_major (majorName),
    kindName       TEXT,
    subName        TEXT       REFERENCES tb_subject (subName),
    result         REAL       DEFAULT NULL
);

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd1001',
                          '江离',
                          '大一',
                          '三班',
                          '信息工程学院',
                          '计算机科学与技术',
                          '期中',
                          '高等数学',
                          90.0
                      );

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd2002',
                          '江只',
                          '大二',
                          '五班',
                          '文法学院',
                          '汉语言文学',
                          '期中',
                          '政治',
                          97.0
                      );

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd3003',
                          '江零',
                          '大三',
                          '三班',
                          '机电工程学院',
                          '测控仪器与技术',
                          '期中',
                          '数学分析',
                          95.0
                      );

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd4004',
                          '江林',
                          '大四',
                          '四班',
                          '经济与管理学院',
                          '市场营销',
                          '期末',
                          '概率论',
                          90.0
                      );

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd1004',
                          '江小',
                          '大一',
                          '四班',
                          '外国语学院',
                          '翻译',
                          '期末',
                          '大学英语',
                          90.0
                      );

INSERT INTO tb_result (
                          stuID,
                          stuName,
                          gradeName,
                          className,
                          departmentName,
                          majorName,
                          kindName,
                          subName,
                          result
                      )
                      VALUES (
                          'xd3004',
                          '江知',
                          '大三',
                          '九班',
                          '信息工程学院',
                          '人工智能',
                          '期中',
                          'ASDF',
                          90.0
                      );


-- 表：tb_student
DROP TABLE IF EXISTS tb_student;

CREATE TABLE IF NOT EXISTS tb_student (
    stuID          TEXT       PRIMARY KEY,
    stuName        TEXT (200) NOT NULL,
    age            INTEGER    DEFAULT NULL
                              NOT NULL,
    sex            TEXT       DEFAULT NULL
                              NOT NULL,
    phone          TEXT       DEFAULT NULL
                              NOT NULL,
    address        TEXT       NOT NULL,
    gradeName      TEXT (200) REFERENCES tb_grade (gradeName),
    className      TEXT (200) REFERENCES tb_class (className),
    departmentName TEXT (200) REFERENCES tb_department (departmentName),
    majorName      TEXT (200) REFERENCES tb_major (majorName) 
);

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd1001',
                           '江离',
                           18,
                           '男',
                           '12387610312',
                           '北京朝阳区',
                           '大一',
                           '三班',
                           '信息工程学院',
                           '计算机科学与技术'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd2002',
                           '江只',
                           19,
                           '男',
                           '12387610319',
                           '天津市河西区',
                           '大二',
                           '五班',
                           '文法学院',
                           '汉语言文学'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd2004',
                           '江晓',
                           20,
                           '男',
                           '12387610309',
                           '湖北省武汉市',
                           '大二',
                           '四班',
                           '生物工程学院',
                           '生物工程'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd3003',
                           '江零',
                           20,
                           '男',
                           '12387610343',
                           '北京海淀区',
                           '大三',
                           '三班',
                           '机电工程学院',
                           '测控仪器与技术'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd3004',
                           '江知',
                           20,
                           '男',
                           '12387610309',
                           '浙江省杭州市',
                           '大三',
                           '九班',
                           '信息工程学院',
                           '人工智能'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd4004',
                           '江林',
                           20,
                           '男',
                           '12387610309',
                           '吉林省长春市',
                           '大四',
                           '四班',
                           '经济与管理学院',
                           '市场营销'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd1004',
                           '江小',
                           19,
                           '女',
                           '111234567901',
                           '浙江省苏州市',
                           '大一',
                           '二班',
                           '外国语学院',
                           '翻译'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd1002',
                           '江语',
                           19,
                           '女',
                           '11',
                           '11',
                           '大一',
                           '二班',
                           '信息工程学院',
                           '123'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd100201',
                           '江宇',
                           19,
                           '男',
                           '11',
                           '11',
                           '大一',
                           '二班',
                           '生物工程学院',
                           '123'
                       );

INSERT INTO tb_student (
                           stuID,
                           stuName,
                           age,
                           sex,
                           phone,
                           address,
                           gradeName,
                           className,
                           departmentName,
                           majorName
                       )
                       VALUES (
                           'xd100301',
                           '江佳',
                           19,
                           '男',
                           '123',
                           '123',
                           '大一',
                           '三班',
                           '文法学院',
                           '345'
                       );


-- 表：tb_subject
DROP TABLE IF EXISTS tb_subject;

CREATE TABLE IF NOT EXISTS tb_subject (
    subID   INTEGER NOT NULL
                    PRIMARY KEY AUTOINCREMENT,
    subName TEXT    NOT NULL
);

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           1,
                           '高等数学'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           2,
                           'python课程设计'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           3,
                           '高等语言C++'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           4,
                           '计算机网络'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           5,
                           '计算机组成原理'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           6,
                           '数据库概论'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           7,
                           '操作系统'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           8,
                           '政治'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           9,
                           '大学英语'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           10,
                           '数学分析'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           11,
                           'ASDF'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           12,
                           '概率论'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           13,
                           '宏观经济学'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           14,
                           '微观经济学'
                       );

INSERT INTO tb_subject (
                           subID,
                           subName
                       )
                       VALUES (
                           15,
                           '算法分析'
                       );


-- 表：tb_user
DROP TABLE IF EXISTS tb_user;

CREATE TABLE IF NOT EXISTS tb_user (
    userName TEXT NOT NULL
                  PRIMARY KEY,
    userPwd  TEXT NOT NULL
);

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'admin',
                        'admin12'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'yj',
                        'yj'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'yu',
                        '12345'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'yyu',
                        'yi123'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'as',
                        'asdf'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        'AAA',
                        'ASDF'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        '江乐',
                        'JL1234'
                    );

INSERT INTO tb_user (
                        userName,
                        userPwd
                    )
                    VALUES (
                        '李佳',
                        'LJ34'
                    );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
