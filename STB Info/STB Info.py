# Test name = Serial Number
# Test description = Check S/N from menu with scanned S/N, log nagraguide version and sw version
from datetime import datetime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

SIGNAL_STRENGTH_THRESHOLD_LOW = NOS_API.SIGNAL_STRENGTH_THRESHOLD_LOW_DSR_7151
SIGNAL_STRENGTH_THRESHOLD_HIGH = NOS_API.SIGNAL_STRENGTH_THRESHOLD_HIGH_DSR_7151
BER_THRESHOLD = NOS_API.BER_THRESHOLD_DSR_7151

def runTest():
    System_Failure = 0
    while(System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            test_result_sn = False
            
            STB_INFO_Result = False
            logistic_serial_number = "-"
            firmware_version = "-"
            nagra_guide_version = "-"
            Signal_Power = "-"
            Signal_Qual = "-"
            cas_id_number = "-"
            sc_number = "-"
            error_codes = ""
            error_messages = ""
            counter = 0
            FIRMWARE_VERSION_PROD = NOS_API.Firmware_Version_DSR_7151
            nagra_guide_version_Prod = NOS_API.Nagra_Guide_Version_DSR_7151
            
            test_result_ver = False 
            signal_strength_ver = "-"
            ber_ver = "-"
            signal_strength_hor = "-"
            ber_hor = "-"
            
            ## Get scanned STB Barcode
            scanned_serial_number = NOS_API.test_cases_results_info.s_n_using_barcode
            scanned_serial_number = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.s_n_using_barcode)

            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            
            if(System_Failure == 1):
                TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                if not(NOS_API.is_signal_present_on_video_source()):
                    test_result = "FAIL"
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                    
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                    
            TEST_CREATION_API.send_ir_rc_command("[Ver_CH]")
            
            if (NOS_API.is_signal_present_on_video_source()):
                TEST_CREATION_API.send_ir_rc_command("[UP]")
                if not(NOS_API.grab_picture("Channel")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                    
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height == "720"):
                    video_result_0 = NOS_API.compare_pictures("black_720_ref", "Channel");
                elif (video_height == "576"):
                    video_result_0 = NOS_API.compare_pictures("black_576_ref", "Channel");
                elif (video_height == "1080"):
                    video_result_0 = NOS_API.compare_pictures("black_1080_ref", "Channel");
                
                if(video_result_0 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    result = 0
                else:
                    result = 3
                
                time_out = 120
                current_time = 0
                start_time = time.localtime()
                while((result >= 0 and result < 3) and current_time < time_out):
                    result = NOS_API.wait_for_multiple_pictures(["black_720_ref", "black_576_ref", "black_1080_ref"], 5, ["[FULL_SCREEN]", "[FULL_SCREEN_576]", "[FULL_SCREEN_1080]"], [80, 80, 80])
                    time.sleep(5)
                    current_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                    TEST_CREATION_API.send_ir_rc_command("[UP]")
                
                if (result >= 0 and result < 3):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)
                   
                    return
                
                time.sleep(1)
                ## Navigate to the Info ZON box menu
                if not(NOS_API.test_cases_results_info.channel_boot_up_state):
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "720"):
                        TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720]")
                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "720"):
                            TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                            time.sleep(1)
                            TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720_slow]")                       
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "720"):
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                                error_codes = NOS_API.test_cases_results_info.resolution_error_code
                                error_messages = NOS_API.test_cases_results_info.resolution_error_message
                                NOS_API.set_error_message("Resolução")
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                    if not(NOS_API.grab_picture("Inst_Error_check")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    video_result = NOS_API.compare_pictures("Inst_error_ref", "Inst_Error_check")
                    video_result_1 = NOS_API.compare_pictures("Inst_Error_ref1", "Inst_Error_check")
                    if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.send_ir_rc_command("[Left]")
                        TEST_CREATION_API.send_ir_rc_command("[Left]")
                        TEST_CREATION_API.send_ir_rc_command("[Left]")
                        TEST_CREATION_API.send_ir_rc_command("[Left]")
                        TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_BOOT_UP_SEQUENCE_Inst]")
                        time.sleep(5)
                        TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_BOOT_UP_SEQUENCE_2]")
                        time.sleep(2)
                        TEST_CREATION_API.send_ir_rc_command("[OK]")
                        time.sleep(3)
                    TEST_CREATION_API.send_ir_rc_command("[Ver_CH]")
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU]")
                if not(NOS_API.grab_picture("Serial_Number_Zone")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = ""    
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                    
                    
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    return
                video_result = NOS_API.compare_pictures("Info_Zon_Box_1_ref", "Serial_Number_Zone", "[Serial_Number]")
                video_result_1 = NOS_API.compare_pictures("Info_Zon_Box_2_ref", "Serial_Number_Zone", "[Serial_Number]")
                if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result_1 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):  
                    TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[Ver_CH]")
                    TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_slow]")
                    if not(NOS_API.grab_picture("Serial_Number_Zone_1")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    video_result = NOS_API.compare_pictures("Info_Zon_Box_1_ref", "Serial_Number_Zone_1", "[Serial_Number]")
                    video_result_1 = NOS_API.compare_pictures("Info_Zon_Box_2_ref", "Serial_Number_Zone_1", "[Serial_Number]")
                    if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result_1 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[Ver_CH]")
                        TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_slow]")
                        if not(NOS_API.grab_picture("Serial_Number_Zone_2")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        video_result = NOS_API.compare_pictures("Info_Zon_Box_1_ref", "Serial_Number_Zone_2", "[Serial_Number]")
                        video_result_1 = NOS_API.compare_pictures("Info_Zon_Box_2_ref", "Serial_Number_Zone_2", "[Serial_Number]")
                        if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and video_result_1 < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            if (TEST_CREATION_API.compare_pictures("Serial_Number_Zone_1", "Serial_Number_Zone_2")):
                                TEST_CREATION_API.write_log_to_file("STB Blocks")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                NOS_API.set_error_message("STB bloqueou")
                                error_codes = NOS_API.test_cases_results_info.block_error_code
                                error_messages = NOS_API.test_cases_results_info.block_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                report_file = ""
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                                return
                            else:
                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                NOS_API.set_error_message("Navegação")
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                while (counter < 3):
                    ## Perform grab picture
                    if not(NOS_API.grab_picture("Info_Zon_Box")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    counter = 3
                    ## Extract serial number from image
                    logistic_serial_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("Info_Zon_Box", "[SERIAL_NUMBER]", "[OCR_FILTER]"))
                    NOS_API.test_cases_results_info.s_n = logistic_serial_number
                    
                    TEST_CREATION_API.write_log_to_file("Logistic serial number barcode: "  + str(scanned_serial_number))
                    TEST_CREATION_API.write_log_to_file("Logistic serial number without barcode: "  + str(logistic_serial_number))
                    
                    ## Check if logistic serial number is the same as scanned serial number
                    if (NOS_API.ignore_zero_letter_o_during_comparation(logistic_serial_number, scanned_serial_number)):
            
                        NOS_API.test_cases_results_info.s_n_ok = True
            
                        ## Set test result to PASS
                        test_result_sn = True
                        TEST_CREATION_API.write_log_to_file("Logistic serial number (from menu):\t" + logistic_serial_number, "logistic_serial_number.txt")
            
                        ## Extract NagraGuide version from image
                        nagra_guide_version = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("Info_Zon_Box", "[NAGRA_GUIDE_VERSION]", "[OCR_FILTER]", "nagra_guide_version"))
                        NOS_API.test_cases_results_info.nagra_guide_version = nagra_guide_version
                        
                        TEST_CREATION_API.write_log_to_file("The extracted nagra guide version is: " + nagra_guide_version)
                        if not(nagra_guide_version == nagra_guide_version_Prod):
                            test_result_sn = False
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                            test_result = "FAIL"
                        
                        ## Extract SW Version from image
                        firmware_version = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("Info_Zon_Box", "[FIRMWARE_VERSION]", "[OCR_FILTER]", "firmware_version"))
                        NOS_API.test_cases_results_info.firmware_version = firmware_version
                        TEST_CREATION_API.write_log_to_file("The extracted firmware version is: " + firmware_version)
                        if not(firmware_version == FIRMWARE_VERSION_PROD):
                            test_result_sn = False
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                            test_result = "FAIL"
                    else:
                        TEST_CREATION_API.write_log_to_file("Logistic serial number is not the same as scanned serial number")
                        
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_s_n_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.wrong_s_n_error_message \
                                                                + "; OCR: " + str(logistic_serial_number))
                        NOS_API.set_error_message("S/N")
                        error_codes = NOS_API.test_cases_results_info.wrong_s_n_error_code
                        error_messages = NOS_API.test_cases_results_info.wrong_s_n_error_message
            else:
                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                NOS_API.set_error_message("Video HDMI")
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                
                
            #################################################### SmartCar Detection ########################################################    
                
            if(test_result_sn):
                
                counter = 0
                if (NOS_API.is_signal_present_on_video_source()):
                    TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_SC_MENU_FROM_INFO_ZON_BOX_MENU]")
                    while (counter < 3):   
                        if not(NOS_API.grab_picture("Signal_Info")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        Signal_Power = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("Signal_Info", "[Signal_Power]", "[OCR_FILTER]", "Signal_Power"))
                        NOS_API.test_cases_results_info.power_percent = str(Signal_Power)
                        Signal_Qual = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("Signal_Info", "[Signal_Qual]", "[OCR_FILTER]", "Signal_Qual"))
                        NOS_API.test_cases_results_info.ber_percent = str(Signal_Qual)
                        
                        TEST_CREATION_API.write_log_to_file("The extracted Signal Power is: " + Signal_Power +"%")
                        TEST_CREATION_API.write_log_to_file("The extracted Signal Quality is: " + Signal_Qual +"%")
                        
                        TEST_CREATION_API.send_ir_rc_command("[NAVIGATE_SC_MENU_FROM_INFO_ZON_BOX_MENU]")
                        
                        ## Perform grab picture
                        if not(NOS_API.grab_picture("sc_info")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        counter = 3
                        video_result = NOS_API.mask_and_compare_pictures("sc_info_ref", "sc_info", "sc_info_mask");
                
                        ## Check is SC not detected
                        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        
                            NOS_API.display_dialog("Reinsira o cart\xe3o e de seguida pressiona Continuar", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
            
                            TEST_CREATION_API.send_ir_rc_command("[REDO_SC]")
                            
                            ## Perform grab picture
                            try:
                                TEST_CREATION_API.grab_picture("sc_info")
                            except: 
                                time.sleep(5)
                                try:
                                    TEST_CREATION_API.grab_picture("sc_info")
                                except:                             
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    test_result = "FAIL"
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                
                
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                    
                                    
                                    
                                    
                                    
                                    return    
                        
                            video_result = NOS_API.mask_and_compare_pictures("sc_info_ref", "sc_info", "sc_info_mask");
                
                            ## Check is SC not detected
                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("Smart card is not detected")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.sc_not_detected_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.sc_not_detected_error_message)
                                NOS_API.set_error_message("SmartCard")
                                error_codes = NOS_API.test_cases_results_info.sc_not_detected_error_code
                                error_messages = NOS_API.test_cases_results_info.sc_not_detected_error_message
                            else:
                    
                                ## Extract text from image
                                sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                                cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                    
                                NOS_API.test_cases_results_info.sc_number = sc_number
                                NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                                NOS_API.test_cases_results_info.cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                    
                                TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                                TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                    
                                NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                        + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                    
                                STB_INFO_Result = True
                                ## System must compare CAS ID number with the CAS ID number previuosly scanned by barcode scanner
                                #if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, NOS_API.test_cases_results_info.cas_id_using_barcode)):
                                #    STB_INFO_Result = True
                                #    NOS_API.test_cases_results_info.correct_cas_id_number = True
                                #else:
                                #    TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                #    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                #                                        + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                #                                        + "; OCR: " + str(cas_id_number))
                                #    NOS_API.set_error_message("CAS ID")
                                #    error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                #    error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message                                   
                        else:              
                            ## Extract text from image
                            sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                            cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                
                            NOS_API.test_cases_results_info.sc_number = sc_number
                            NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                            NOS_API.test_cases_results_info.cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                
                            TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                            TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                
                            NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                    + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                
                            STB_INFO_Result = True
                            ## System must compare CAS ID number with the CAS ID number previuosly scanned by barcode scanner
                            #if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, NOS_API.test_cases_results_info.cas_id_using_barcode)):
                            #    STB_INFO_Result = True
                            #    NOS_API.test_cases_results_info.correct_cas_id_number = True
                            #else:
                            #    TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                            #    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                            #                                        + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                            #                                        + "; OCR: " + str(cas_id_number))
                            #    NOS_API.set_error_message("CAS ID")
                            #    error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                            #    error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message
                else:
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")    
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
       
             #################################################### Ver_Hor Channel  ########################################################
             
            if(STB_INFO_Result):
                counter = 0
                video_result = 0
                time.sleep(2)
                if (NOS_API.is_signal_present_on_video_source()):
                    TEST_CREATION_API.send_ir_rc_command("[Ver_Hor_Check]")
                    time.sleep(2)
                    if not(NOS_API.grab_picture("Vertical_Zone")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = ""    
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        return
                    video_result = NOS_API.compare_pictures("Signal_Info_ref", "Vertical_Zone", "[Ver_Pol_Zone]")
                    if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                        time.sleep(1)
                        TEST_CREATION_API.send_ir_rc_command("[ZAP_SEQUENCE]")
                        if not(NOS_API.grab_picture("Vertical_Zone_1")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        video_result = NOS_API.compare_pictures("Signal_Info_ref", "Vertical_Zone_1", "[Ver_Pol_Zone]")
                        if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                            time.sleep(1)
                            TEST_CREATION_API.send_ir_rc_command("[ZAP_SEQUENCE_slow]")
                            if not(NOS_API.grab_picture("Vertical_Zone_2")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                            video_result = NOS_API.compare_pictures("Signal_Info_ref", "Vertical_Zone_2", "[Ver_Pol_Zone]")
                            if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                if (TEST_CREATION_API.compare_pictures("Vertical_Zone_1", "Vertical_Zone_2")):
                                    TEST_CREATION_API.write_log_to_file("STB Blocks")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.block_error_message)
                                    NOS_API.set_error_message("STB bloqueou")
                                    error_codes = NOS_API.test_cases_results_info.block_error_code
                                    error_messages = NOS_API.test_cases_results_info.block_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                    report_file = ""
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                                    return
                                else:
                                    TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                    NOS_API.set_error_message("Navegação")
                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = ""    
                                    if (test_result != "PASS"):
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    return
                        time.sleep(2)
                    while (counter < 3):                    
                        ## Perform grab picture
                        if not(NOS_API.grab_picture("Signal_Info_Ver")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                        
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            return
                        if not (TEST_CREATION_API.compare_pictures("Signal_Info_ref", "Signal_Info_Ver", "[CubaV_Check]")):
                            TEST_CREATION_API.send_ir_rc_command("[Ver_CH]")
                            time.sleep(3)
                            if not(NOS_API.grab_picture("Signal_Info_Ver")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                            if not (TEST_CREATION_API.compare_pictures("Signal_Info_ref", "Signal_Info_Ver", "[CubaV_Check]")):
                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                NOS_API.set_error_message("Navegação")
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - " + str(signal_strength_hor) + " " + ber_hor + " " + str(signal_strength_ver) + " " + ber_ver + " - - - - - - - - -",
                                                "- - - - - - - >" + str(SIGNAL_STRENGTH_THRESHOLD_LOW) + "<" + str(SIGNAL_STRENGTH_THRESHOLD_HIGH) + " " + str(BER_THRESHOLD) + " >" + str(SIGNAL_STRENGTH_THRESHOLD_LOW) + "<" + str(SIGNAL_STRENGTH_THRESHOLD_HIGH) + " " + str(BER_THRESHOLD) + " - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                return
                        counter = 3
                        signal_strength_ver = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("Signal_Info_Ver", "[Hor/Ver]", "[OCR_FILTER]", "Ver"))
                        try:
                            result_float = True
                            signal_strength_ver = float(signal_strength_ver)
                            NOS_API.test_cases_results_info.power_vertical_polarization = str(signal_strength_ver)
                        except ValueError:
                            result_float= False
                        
                        if(signal_strength_ver == ""  or result_float == False):
                            signal_strength_ver = 0
                            NOS_API.test_cases_results_info.power_vertical_polarization = "-"
                        #if not(NOS_API.represent_float(signal_strength)):
                        #    signal_strength = 17
                        #else:
                        #    signal_strength = float(signal_strength)
                        TEST_CREATION_API.write_log_to_file("Power vertical polarization: " + str(signal_strength_ver) + "dBuV")
                        NOS_API.update_test_slot_comment("Power vertical polarization: " + str(signal_strength_ver) + "dBuV")
                        
                        if (signal_strength_ver > SIGNAL_STRENGTH_THRESHOLD_LOW and signal_strength_ver < SIGNAL_STRENGTH_THRESHOLD_HIGH):
                            try:
                                ber_ver = NOS_API.fix_ber(TEST_CREATION_API.OCR_recognize_text("Signal_Info_Ver", "[Ber]", "[OCR_FILTER]"))
                                TEST_CREATION_API.write_log_to_file("BER vertical polarization: " + ber_ver)
                                NOS_API.update_test_slot_comment("BER vertical polarization: " + ber_ver)
                                NOS_API.test_cases_results_info.ber_vertical_polarization = ber_ver
                            except Exception as error:
                                ## Set test result to INCONCLUSIVE
                                TEST_CREATION_API.write_log_to_file(str(error))
                                ber_ver = "-1"
                                NOS_API.test_cases_results_info.ber_vertical_polarization = "-"
                                                   
                        #if (signal_strength_ver > SIGNAL_STRENGTH_THRESHOLD_LOW and signal_strength_ver < SIGNAL_STRENGTH_THRESHOLD_HIGH):
                            if (NOS_API.check_ber(ber_ver, BER_THRESHOLD)):
                                test_result_ver = True
                                break
                            else:
                                TEST_CREATION_API.write_log_to_file("Ber on vertical polarization")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ber_vertical_polarization_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.ber_vertical_polarization_error_message)
                                NOS_API.set_error_message("Tuner") 
                                error_codes = NOS_API.test_cases_results_info.ber_vertical_polarization_error_code
                                error_messages = NOS_API.test_cases_results_info.ber_vertical_polarization_error_message
                        else:
                            TEST_CREATION_API.write_log_to_file("Power on vertical polarization")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_vertical_polarization_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_vertical_polarization_error_message)
                            NOS_API.set_error_message("Tuner")
                            error_codes = NOS_API.test_cases_results_info.power_vertical_polarization_error_code
                            error_messages = NOS_API.test_cases_results_info.power_vertical_polarization_error_message
                else:
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message  

                ################################################ Horizontal Polarization Test ##################################################
                    
                if(test_result_ver):
                    counter = 0
                    video_result = 0
                    time.sleep(3)
                    if (NOS_API.is_signal_present_on_video_source()):
                        ## Zap to horizontal polarization channel
                        TEST_CREATION_API.send_ir_rc_command("[Hor_CH]")
                        
                        time.sleep(3)
                        while (counter < 3):       
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("Signal_Info_Hor")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                            
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                return
                            counter = 3
                            signal_strength_hor  = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("Signal_Info_Hor", "[Hor/Ver]", "[OCR_FILTER]", "Hor"))
                            try:
                                result_float = True
                                signal_strength_hor  = float(signal_strength_hor)
                                NOS_API.test_cases_results_info.power_horizontal_polarization = str(signal_strength_hor)
                            except ValueError:
                                result_float= False
                            
                            if(signal_strength_hor  == ""  or result_float == False):
                                signal_strength_hor  = 0
                                NOS_API.test_cases_results_info.power_horizontal_polarization = "-"
                            #if not(NOS_API.represent_float(signal_strength)):
                                #signal_strength = 17
                            #else:
                                #signal_strength = float(signal_strength)                            
                            
                            TEST_CREATION_API.write_log_to_file("Power horizontal polarization: " + str(signal_strength_hor ) + "dBuV")
                            NOS_API.update_test_slot_comment("Power horizontal polarization: " + str(signal_strength_hor ) + "dBuV")                        
                            
                            if (signal_strength_hor  > SIGNAL_STRENGTH_THRESHOLD_LOW and signal_strength_hor  < SIGNAL_STRENGTH_THRESHOLD_HIGH):
                                try:
                                    ber_hor = NOS_API.fix_ber(TEST_CREATION_API.OCR_recognize_text("Signal_Info_Hor", "[Ber]", "[OCR_FILTER]"))
                                    TEST_CREATION_API.write_log_to_file("BER horizontal polarization: " + ber_hor )
                                    NOS_API.update_test_slot_comment("BER horizontal polarization: " + ber_hor )
                                    NOS_API.test_cases_results_info.ber_horizontal_polarization = ber_hor                   
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    ber_hor  = "-1"
                                    NOS_API.test_cases_results_info.ber_horizontal_polarization = "-"
                            #if (signal_strength_hor  > SIGNAL_STRENGTH_THRESHOLD_LOW and signal_strength_hor  < SIGNAL_STRENGTH_THRESHOLD_HIGH):
                                if (NOS_API.check_ber(ber_hor , BER_THRESHOLD)):
                                    test_result = "PASS"
                                    TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                                    break
                                else:
                                    TEST_CREATION_API.write_log_to_file("Ber on horizontal polarization")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ber_horizontal_polarization_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.ber_horizontal_polarization_error_message)
                                    NOS_API.set_error_message("Tuner") 
                                    error_codes = NOS_API.test_cases_results_info.ber_horizontal_polarization_error_code
                                    error_messages = NOS_API.test_cases_results_info.ber_horizontal_polarization_error_message
                            else:
                                TEST_CREATION_API.write_log_to_file("Power on horizontal polarization")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_horizontal_polarization_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.power_horizontal_polarization_error_message)
                                NOS_API.set_error_message("Tuner")
                                error_codes = NOS_API.test_cases_results_info.power_horizontal_polarization_error_code
                                error_messages = NOS_API.test_cases_results_info.power_horizontal_polarization_error_message   
                    else:
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message    
            ################################################################################################################################          
            
            System_Failure = 2
            
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection")
                System_Failure = 2

    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - " + str(Signal_Power) + " " + str(Signal_Qual) + " - - - " + str(signal_strength_hor) + " " + ber_hor + " " + str(signal_strength_ver) + " " + ber_ver + " " + str(logistic_serial_number) + " " + str(cas_id_number) + " " + str(firmware_version) + " " + str(nagra_guide_version) + " " + str(sc_number) + " - - - -",
                    "- - - - - - - >" + str(SIGNAL_STRENGTH_THRESHOLD_LOW) + "<" + str(SIGNAL_STRENGTH_THRESHOLD_HIGH) + " " + str(BER_THRESHOLD) + " >" + str(SIGNAL_STRENGTH_THRESHOLD_LOW) + "<" + str(SIGNAL_STRENGTH_THRESHOLD_HIGH) + " " + str(BER_THRESHOLD) + " - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_file = ""
    if (test_result != "PASS"):
        report_file = NOS_API.create_test_case_log_file(
                        NOS_API.test_cases_results_info.s_n_using_barcode,
                        NOS_API.test_cases_results_info.nos_sap_number,
                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                        "",
                        end_time)
        NOS_API.upload_file_report(report_file)
        NOS_API.test_cases_results_info.isTestOK = False
        
        NOS_API.send_report_over_mqtt_test_plan(
                test_result,
                end_time,
                error_codes,
                report_file)

    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()
   