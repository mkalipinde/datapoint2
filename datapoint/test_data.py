import json


class data:

    def testData():
        data = {
            "process_id": 9,
            "approval_stages": [
                {
                    "pk_approval_roleid": 121,
                    "process_approval_stage": {
                        "pk_process_approval_stageid": 26,
                        "approval_stage": {
                            "pk_approval_stageid": 2,
                            "approval_stage": "Initiate a request",
                            "approval_code": "Initiate a request"
                        },
                        "process": {
                            "pk_processid": 9,
                            "process_categoryid": {
                                "pk_process_categoryid": 3,
                                "process_category": "Information System"
                            },
                            "process": "IT Equipment",
                            "process_code": "IE",
                            "fk_process_categoryid": 3
                        },
                        "approval_stage_number": 1,
                        "approval_stage_status": "Active",
                        "fk_processid": 9,
                        "fk_approval_stageid": 2
                    },
                    "role": {
                        "pk_roleid": 50,
                        "role": "Initiator",
                        "description": "All users in the system"
                    },
                    "fk_process_approval_stageid": 26,
                    "fk_roleid": 50
                },
                {
                    "pk_approval_roleid": 2,
                    "process_approval_stage": {
                        "pk_process_approval_stageid": 41,
                        "approval_stage": {
                            "pk_approval_stageid": 3,
                            "approval_stage": "Approval",
                            "approval_code": "Approval"
                        },
                        "process": {
                            "pk_processid": 9,
                            "process_categoryid": {
                                "pk_process_categoryid": 3,
                                "process_category": "Information System"
                            },
                            "process": "IT Equipment",
                            "process_code": "IE",
                            "fk_process_categoryid": 3
                        },
                        "approval_stage_number": 2,
                        "approval_stage_status": "Active",
                        "fk_processid": 9,
                        "fk_approval_stageid": 3
                    },
                    "role": {
                        "pk_roleid": 1,
                        "role": "Administrator",
                        "description": "Super user of the system with all the rights"
                    },
                    "fk_process_approval_stageid": 41,
                    "fk_roleid": 1
                },
                {
                    "pk_approval_roleid": 32,
                    "process_approval_stage": {
                        "pk_process_approval_stageid": 192,
                        "approval_stage": {
                            "pk_approval_stageid": 4,
                            "approval_stage": "Implementation",
                            "approval_code": "Implementation"
                        },
                        "process": {
                            "pk_processid": 9,
                            "process_categoryid": {
                                "pk_process_categoryid": 3,
                                "process_category": "Information System"
                            },
                            "process": "IT Equipment",
                            "process_code": "IE",
                            "fk_process_categoryid": 3
                        },
                        "approval_stage_number": 3,
                        "approval_stage_status": "Active",
                        "fk_processid": 9,
                        "fk_approval_stageid": 4
                    },
                    "role": {
                        "pk_roleid": 4,
                        "role": "Administration and Finance Manager",
                        "description": "Administration and Finance Manager"
                    },
                    "fk_process_approval_stageid": 192,
                    "fk_roleid": 4
                }
            ],
            "process_stage_approvers": [
                {
                    "pk_process_stage_approverid": 74,
                    "profile": {
                        "pk_profileid": 98,
                        "user": {
                            "id": 4,
                            "first_name": "Martin",
                            "last_name": "MSIMUKO",
                            "email": "Martin.MSIMUKO@total.co.mw",
                            "username": "J0242133"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 32,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 192,
                            "approval_stage": {
                                "pk_approval_stageid": 4,
                                "approval_stage": "Implementation",
                                "approval_code": "Implementation"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 3,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 4
                        },
                        "role": {
                            "pk_roleid": 4,
                            "role": "Administration and Finance Manager",
                            "description": "Administration and Finance Manager"
                        },
                        "fk_process_approval_stageid": 192,
                        "fk_roleid": 4
                    },
                    "approver_status": "Active",
                    "approver_level": 1,
                    "fk_profileid": 98,
                    "fk_approval_roleid": 32
                },
                {
                    "pk_process_stage_approverid": 8,
                    "profile": {
                        "pk_profileid": 95,
                        "user": {
                            "id": 1,
                            "first_name": "Joel",
                            "last_name": "Kumwenda",
                            "email": "jkumwenda@gmail.com",
                            "username": "jkumwenda"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": False
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 1,
                    "fk_profileid": 95,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 75,
                    "profile": {
                        "pk_profileid": 217,
                        "user": {
                            "id": 123,
                            "first_name": "Bright",
                            "last_name": "EGBUKICHI",
                            "email": "Bright.EGBUKICHI@total.co.mw",
                            "username": "J0249697"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 32,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 192,
                            "approval_stage": {
                                "pk_approval_stageid": 4,
                                "approval_stage": "Implementation",
                                "approval_code": "Implementation"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 3,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 4
                        },
                        "role": {
                            "pk_roleid": 4,
                            "role": "Administration and Finance Manager",
                            "description": "Administration and Finance Manager"
                        },
                        "fk_process_approval_stageid": 192,
                        "fk_roleid": 4
                    },
                    "approver_status": "Active",
                    "approver_level": 2,
                    "fk_profileid": 217,
                    "fk_approval_roleid": 32
                },
                {
                    "pk_process_stage_approverid": 9,
                    "profile": {
                        "pk_profileid": 99,
                        "user": {
                            "id": 5,
                            "first_name": "Caroline",
                            "last_name": "MUTETI",
                            "email": "Caroline.MUTETI@total.co.mw",
                            "username": "J0461159"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 2,
                    "fk_profileid": 99,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 10,
                    "profile": {
                        "pk_profileid": 142,
                        "user": {
                            "id": 48,
                            "first_name": "Davies",
                            "last_name": "MSAKAMBEWA",
                            "email": "Davies.MSAKAMBEWA@total.co.mw",
                            "username": "J1006255"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 3,
                    "fk_profileid": 142,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 11,
                    "profile": {
                        "pk_profileid": 177,
                        "user": {
                            "id": 83,
                            "first_name": "Micaiah",
                            "last_name": "NKOMBA",
                            "email": "Micaiah.NKOMBA@total.co.mw",
                            "username": "J0491436"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 4,
                    "fk_profileid": 177,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 12,
                    "profile": {
                        "pk_profileid": 194,
                        "user": {
                            "id": 100,
                            "first_name": "William",
                            "last_name": "MBOWE",
                            "email": "William.MBOWE@total.co.mw",
                            "username": "J0517671"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 5,
                    "fk_profileid": 194,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 13,
                    "profile": {
                        "pk_profileid": 208,
                        "user": {
                            "id": 114,
                            "first_name": "Humphrey",
                            "last_name": "Kumwembe",
                            "email": "hkumwembe@gmail.com",
                            "username": "hkumwembe"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 6,
                    "fk_profileid": 208,
                    "fk_approval_roleid": 2
                },
                {
                    "pk_process_stage_approverid": 14,
                    "profile": {
                        "pk_profileid": 225,
                        "user": {
                            "id": 131,
                            "first_name": "Patrick",
                            "last_name": "Kalamula",
                            "email": "patrick@patkay.net",
                            "username": "patrick@patkay.net"
                        },
                        "mobile": "088888888",
                        "profile_img": "img",
                        "status": True
                    },
                    "approval_role": {
                        "pk_approval_roleid": 2,
                        "process_approval_stage": {
                            "pk_process_approval_stageid": 41,
                            "approval_stage": {
                                "pk_approval_stageid": 3,
                                "approval_stage": "Approval",
                                "approval_code": "Approval"
                            },
                            "process": {
                                "pk_processid": 9,
                                "process_categoryid": {
                                    "pk_process_categoryid": 3,
                                    "process_category": "Information System"
                                },
                                "process": "IT Equipment",
                                "process_code": "IE",
                                "fk_process_categoryid": 3
                            },
                            "approval_stage_number": 2,
                            "approval_stage_status": "Active",
                            "fk_processid": 9,
                            "fk_approval_stageid": 3
                        },
                        "role": {
                            "pk_roleid": 1,
                            "role": "Administrator",
                            "description": "Super user of the system with all the rights"
                        },
                        "fk_process_approval_stageid": 41,
                        "fk_roleid": 1
                    },
                    "approver_status": "Active",
                    "approver_level": 7,
                    "fk_profileid": 225,
                    "fk_approval_roleid": 2
                }
            ],
            "status": 1,
            "fk_requestid": 3461,
            "comment": "This is a comment",
            "isDenied": 0
        }
        return data
