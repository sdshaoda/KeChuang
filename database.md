## 1. 数据表

- announcements_announcement：公告信息
- announcements_document：公文信息
- auth_group：Django中组信息
- auth_group_permissions：Django中组权限信息
- auth_permission：Django中权限信息
- captcha_captchastore：验证码的相关信息
- django_admin_log：Django日志记录
- django_content_type：Django文件目录
- django_migrations：Django中数据迁移
- django_session：Django中会话信息
- equipments_equipment：设备信息
- equipments_equipmenttype：设备类型信息
- operation_equipmentapply：设备申请信息
- operation_projectattendance：工程考勤信息
- operation_projectequipment：工程设备信息
- operation_projectmember：工程成员信息
- projects_project：工程信息
- projects_projectstage：项目阶段信息
- projects_projecttype：工程类型信息
- users_department：部门信息
- users_userprofile：用户信息
- users_userprofile_groups：Django用户组信息
- users_userprofile_permissions：Django用户权限信息
- xadmin_bookmark：Xadmin
- xadmin_log：Xadmin的日志记录
- xadmin_usersettings：Xadmin的用户设置信息
- xadmin_userwidget：Xadmin控件信息

## 2. 字段

### announcements_announcement

- id：公告id
- person_name：发布者姓名
- department_name：相关部门
- title：标题
- content：内容
- remark：备注
- add_time：添加时间
- department_id：相关部门id
- person_id：发布者id

### announcements_document

- id：公文id
- person_name：发布者id
- department_name：相关部门
- name：公文名称
- document：公文文件
- remark：备注
- add_time：添加时间
- department_id：相关部门id
- person_id：发布者id

### equipments_equipment

- id：设备id
- equ_type_name：设备类型名称
- equ_name：设备名称
- equ_person_id：设备负责人id
- equ_person：设备负责人姓名
- file_num：档案编号
- equ_num：设备型号
- equ_status：设备状态
- number：设备编号
- biaodingzs：标定证书
- biaoding_date：标定日期
- effect_date：计量有效期
- equ_money：购买价格
- buy_date：购买日期
- use_status：使用状态
- equ_staff_id：设备保管人id
- equ_staff：设备保管人姓名
- department_id：所在部门id
- department：所在部门
- use_date：领用时间
- revert_date：归还时间
- remark：备注
- add_time：添加时间
- equ_type_id：设备类型id

### equipments_equipmenttype

- id：设备类型id
- name：设备类型名称
- remark：备注
- add_time：添加时间

### operation_equipmentapply

- id：设备申请id
- equipment_name：设备名称
- person_name：申请人姓名
- equipment_person_id：设备负责人id
- equipment_person：设备负责人姓名
- type：申请类型
- status：审核状态
- use_date：领用日期
- revert_date：归还日期
- remark：备注
- add_time：添加时间
- equipment_id：设备id
- person_id：申请人id

### operation_projectapply

- id：工程申请id
- project_name：工程名称
- person_name：申请人姓名
- type：申请类型
- status：审核状态
- pro_type_id：工程类型id
- pro_stage_id：项目阶段id
- department_id：部门id
- pro_person_id：工程负责人id
- wt_person_id：法人委托id
- ht_person_id：合同签署人id
- pro_type：工程类型
- pro_stage：项目阶段
- department：所属部门
- pro_person：工程负责人
- wt_person：法人委托
- ht_person：合同签署人
- ht_name：合同名称
- ht_num：合同编号
- ht_money：合同金额
- js_money：结算金额
- wt_dw：委托单位
- mobile：联系电话
- pro_address：项目地址
- sign_date：签订日期
- start_date：开工日期
- finish_date：完工日期
- ht_scan：合同扫描件
- remark：备注
- add_time：添加时间
- person_id：申请人id
- project_id：工程id

### operation_projectattendance

- id：工程考勤id
- project_name：工程名称
- person_name：考勤人员姓名
- department_id：所属部门id
- department：所属部门
- location：地点
- time：时间
- remark：备注
- add_time：添加时间
- person_id：考勤人员id
- project_id：工程id

### operation_projectequipment

- id：工程设备id
- project_name：工程名称
- equipment_name：设备名称
- remark：备注
- add_time：添加时间
- equipment_id：设备id
- project_id：工程id

### operation_projectmember

- id：工程成员id
- project_name：工程名称
- person_name：成员姓名
- is_pro_person：是否为负责人
- department：所属部门名称
- department_id：所属部门id
- remark：备注
- add_time：添加时间
- person_id：成员id
- project_id：工程id

### projects_project

- id：工程id
- pro_type_name：工程类型名称
- pro_stage_name：项目阶段名称
- pro_name：工程名称
- is_active：是否激活
- department_id：所属部门id
- pro_person_id：工程负责人id
- wt_person_id：法人委托id
- ht_person_id：合同签署人id
- pro_person：工程负责人
- department：所属部门
- wt_person：法人委托姓名
- ht_person：合同签署人姓名
- ht_name：合同名称
- ht_num：合同编号
- ht_money：合同金额
- js_money：结算金额
- wt_dw：委托单位
- mobile：联系电话
- pro_address：项目地址
- sign_date：签订日期
- start_date：开工日期
- finish_date：完工日期
- ht_scan：合同扫描件
- remark：备注
- add_time：添加时间
- pro_stage_id：项目阶段id
- pro_type_id：工程类型id

### projects_projectstage

- id：项目阶段id
- name：项目阶段名称
- remark：备注
- add_time：添加时间

### projects_projecttype

- id：工程类型id
- name：工程名称id
- remark：备注
- add_time：添加时间

### users_department

- id：部门id
- name：部门名称
- is_department：部门状态，默认为1
- remark：备注
- add_time：添加时间

### users_userprofile

- id：用户id
- password：密码
- last_login：最后一次登录时间
- is_superuser：超级管理员，默认为0
- first_name：名
- last_name：姓
- is_staff：是否可登录后台管理系统，默认为0
- is_active：是否激活，默认为1
- date_joined：添加时间
- department_name：所在部门名称
- name：姓名
- username：登录名
- sex：性别
- age：年龄
- job：职位
- induction_time：入职时间
- permission：系统权限
- number：人员编号
- identity_num：身份证号
- mobile：手机号
- email：邮箱
- office_phone：办公电话
- home_phone：家庭电话
- home_address：家庭住址
- xueli：学历
- zhicheng：职称
- zige：资格
- identity_image：身份证照片
- person_image：个人照片
- zigezs：资格证书
- xuelizs：学历证书
- zhichengzs：职称证书
- add_time：添加时间
- department_id：所在部门id
- resume：简历
