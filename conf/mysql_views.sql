#sendtaskview
create or replace view sms_sendtaskview as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview01 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask01 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview02 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask02 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview03 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask03 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview04 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask04 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview05 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask05 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview06 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask06 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview07 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask07 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview08 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask08 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview09 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask09 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview10 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask10 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview11 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask11 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_sendtaskview12 as select a.*,b.name user_name,c.root_id cust_id from sms_sendtask12 a left join base_user b on a.user_id=b.id left join base_dept c on b.dept_id=c.id;


#msgsendview
create or replace view sms_msgsendview as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview01 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend01 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview02 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend02 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview03 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend03 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview04 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend04 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview05 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend05 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview06 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend06 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview07 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend07 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview08 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend08 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview09 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend09 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview10 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend10 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview11 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend11 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;
create or replace view sms_msgsendview12 as select a.*,b.name msg_user_name,c.root_id cust_id from sms_msgsend12 a left join base_user b on a.msg_user_id=b.id left join base_dept c on b.dept_id=c.id;


#address view
create or replace view addr_addressview as select a.*,b.name group_name,b.user_id group_user_id,b.dept_id group_dept_id,b.mod group_mod,c.root_id cust_id from addr_address a left join addr_addressgroup b on a.group_id=b.id left join base_dept c on b.dept_id=c.id;