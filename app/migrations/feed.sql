INSERT INTO `access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES 
        ('operator-create', 'operator-create', 1560853801, 1560853801), 
        ('operator-delete', 'operator-delete', 1560853801, 1560853801), 
        ('operator-update', 'operator-update', 1560853801, 1560853801), 
        ('operator-view', 'operator-view', 1560853801, 1560853801),
        ('dashboard-view', 'dashboard-view', 1560853801, 1560853801)
        ('settings-view', 'settings-viewpython3 m', 1560853801, 1560853801);
INSERT INTO `access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES 
        ('log-create', 'log-create', 1560853801, 1560853801), 
        ('log-delete', 'log-delete', 1560853801, 1560853801), 
        ('log-update', 'log-update', 1560853801, 1560853801), 
        ('log-view', 'log-view', 1560853801, 1560853801);
INSERT INTO `access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES 
        ('organizations-create', 'organizations-create', 1560853801, 1560853801), 
        ('organizations-delete', 'organizations-delete', 1560853801, 1560853801), 
        ('organizations-update', 'organizations-update', 1560853801, 1560853801), 
        ('organizations-view', 'organizations-view', 1560853801, 1560853801);
INSERT INTO `access_permissions` (`access_permission_name`, `access_permission_details`, `access_permission_created_at`, `access_permission_updated_at`) VALUES 
        ('tickets-create', 'tickets-create', 1560853801, 1560853801), 
        ('tickets-delete', 'tickets-delete', 1560853801, 1560853801), 
        ('tickets-update', 'tickets-update', 1560853801, 1560853801), 
        ('tickets-view', 'tickets-view', 1560853801, 1560853801);

INSERT INTO `operators` (`operator_id`, `operator_username`, `operator_auth_key`, `operator_password`, `operator_password_reset_token`, `operator_type`, `operator_company_id`, `operator_first_name`, `operator_last_name`, `operator_gender`, `operator_email_id`, `operator_phone_number`, `operator_address`, `operator_profile_photo`, `operator_signature`, `operator_buses`, `operator_organization`, `operator_ip_address`, `operator_created_at`, `operator_created_by`, `operator_updated_at`, `operator_updated_by`, `operator_status`) VALUES
(1, 'support@qtsoftwareltd.com', 'hdYuTBbYj6_Lho3REkSYJUJkMQqlDdIG', '$2y$13$F87lowlE6sdQE.kpQby8Puf2Jsfqtm4Ud6fMSfu8fDVZ3nPKPMG1u', '', 2, 0, 'QTS', 'Support', 0, 'support@qtsoftwareltd.com', '', '', '', '', '', '0', '127.0.0.1', 1570112959, 1, 1650367381, 1, 3),
(2, 'system@qtsoftwareltd.com', 'hdYuTBbYj6_Lho3REkSYJUJkMQqlDdIH', '$2y$13$/3Ur0L1z7b3ma4RDwdld8.DQ4/9GmmRbpscCXL1z42o8cNMb6UfZK', '', 2, 0, 'QTS', 'Support', 0, 'support@qtsoftwareltd.com', '+250726875122', '', '', '', '', '0', '::1', 1570112959, 1, 1590351988, 1, 3);

INSERT INTO `operators` (`operator_id`, `operator_username`, `operator_auth_key`, `operator_password`, `operator_password_reset_token`, `operator_type`, `operator_company_id`, `operator_first_name`, `operator_last_name`, `operator_gender`, `operator_email_id`, `operator_phone_number`, `operator_address`, `operator_profile_photo`, `operator_signature`, `operator_buses`, `operator_organization`, `operator_ip_address`, `operator_created_at`, `operator_created_by`, `operator_updated_at`, `operator_updated_by`, `operator_status`) VALUES
(2, 'system@qtsoftwareltd.com', 'hdYuTBbYj6_Lho3REkSYJUJkMQqlDdIH', '$2y$13$/3Ur0L1z7b3ma4RDwdld8.DQ4/9GmmRbpscCXL1z42o8cNMb6UfZK', '', 2, 0, 'QTS', 'Support', 0, 'support@qtsoftwareltd.com', '+250726875122', '', '', '', '', '0', '::1', 1570112959, 1, 1590351988, 1, 3);


 INSERT INTO `operator_access_permissions` (`operator_access_permission_name`, `operator_access_permission_operator_id`, `operator_access_permission_created_at`, `operator_access_permission_updated_at`) VALUES 
        ('operator-create', '1', '1560853801', '1560853801'),
        ('operator-delete', '1', '1560853801', '1560853801'),
        ('operator-update', '1', '1560853801', '1560853801'),
        ('operator-view', '1', '1560853801', '1560853801'),
        ('dashboard-view', '1', '1560853801', '1560853801'),
        ('settings-view', '1', '1560853801', '1560853801');