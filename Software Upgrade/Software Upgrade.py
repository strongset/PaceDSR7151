# Test name = Software Upgrade
# Test description = Set environment, perform software upgrade and check STB after sw upgrade

from datetime import datetime
import time
import device
import TEST_CREATION_API
import shutil
import os.path
import sys
#import NOS_API

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API
    
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass
    
## Number of alphanumeric characters in SN
SN_LENGTH = 14  

## Number of alphanumeric characters in Cas_Id
CASID_LENGTH = 12
    
## Dialog stays forever until operator press some buttons on dialog
DIALOG_STAYS_FOREVER = 0

##Time to to performe SW upgrade (in seconds)
BOOT_TIME = 60

##Set correct grabber for this TestSlot
NOS_API.grabber_type()

##Set correct grabber for this TestSlot
TEST_CREATION_API.grabber_type()

def runTest():
    
    System_Failure = 0

    while(System_Failure < 2):
        try:
            
            NOS_API.read_thresholds()

            NOS_API.reset_test_cases_results_info()  
        
            ## Set test result default to FAIL
            test_result = "FAIL"
            
            error_codes = ""
            error_messages = ""
            
            SN_LABEL = False
            CASID_LABEL = False
            
            result = 0
               
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
                time.sleep(1)
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
                time.sleep(1)
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
            
            try:
                ## Read STB Labels using barcode reader (S/N, CAS ID) and LOG it             
                all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()
                NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]
                #NOS_API.test_cases_results_info.cas_id_using_barcode = all_scanned_barcodes[2]
                NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
            except Exception as error:
                test_result = "FAIL"
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
                    
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
                
                NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
            
                return
                
            test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
            device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
                
            if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit())):
                SN_LABEL = True
            
            #if ((len(NOS_API.test_cases_results_info.cas_id_using_barcode) == CASID_LENGTH) and (NOS_API.test_cases_results_info.cas_id_using_barcode.isalnum() or NOS_API.test_cases_results_info.cas_id_using_barcode.isdigit())):
            #    CASID_LABEL = True
            
            #if not(SN_LABEL and CASID_LABEL):
            if not(SN_LABEL):
                TEST_CREATION_API.write_log_to_file("Labels Scaning")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
                
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
            
            counter = 0
            delta_time = 0
            if(System_Failure == 0):
                if not(NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                    TEST_CREATION_API.write_log_to_file("Conectores NOK")
                    NOS_API.set_error_message("Danos Externos") 
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message) 
                    error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                    error_messages = NOS_API.test_cases_results_info.conector_nok_error_message 
                    
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
                if not(NOS_API.display_new_dialog("Painel Traseiro?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                    TEST_CREATION_API.write_log_to_file("Back Panel NOK")
                    NOS_API.set_error_message("Danos Externos") 
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.back_panel_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.back_panel_nok_error_message) 
                    error_codes = NOS_API.test_cases_results_info.back_panel_nok_error_code
                    error_messages = NOS_API.test_cases_results_info.back_panel_nok_error_message 
                    
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
                if not(NOS_API.display_new_dialog("Inserir SmartCard! A STB est\xe1 ligada?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                    TEST_CREATION_API.write_log_to_file("No Power")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message)
                    NOS_API.set_error_message("Não Liga")
                    error_codes = NOS_API.test_cases_results_info.no_power_error_code
                    error_messages = NOS_API.test_cases_results_info.no_power_error_message
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
            
            NOS_API.grabber_hour_reboot()
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()      
            
            ## Start grabber device with video on default video source                                                                                      
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            
            ## Check if have image on HDMI after sw upgrade
            start_time = time.localtime()                            
            while(delta_time < BOOT_TIME):
                time.sleep(1)
                if (NOS_API.is_signal_present_on_video_source()):
                    time.sleep(3)
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    TEST_CREATION_API.write_log_to_file("video_height: "  + str(video_height))
                    TEST_CREATION_API.write_log_to_file("counter: "  + str(counter))
                    if (video_height != "576" and video_height != "720" and video_height != "1080"):
                        time.sleep(45)
                        continue
                    if (video_height == "720" and counter < 4):
                        if(NOS_API.grab_picture("boot_up_stage_hdmi")):
                                            
                            video_result = NOS_API.mask_and_compare_pictures("installation_boot_up_ref", "boot_up_stage_hdmi", "File-MASK")
                            video_result_0 = NOS_API.mask_and_compare_pictures("installation_boot_up_Eng_ref", "boot_up_stage_hdmi", "File-MASK_Eng")
                            video_result_1 = NOS_API.compare_pictures("No_Upgrade", "boot_up_stage_hdmi")
                            video_result_2 = NOS_API.compare_pictures("No_Upgrade_1", "boot_up_stage_hdmi")
                            if(video_result >= NOS_API.thres or video_result_0 >= NOS_API.thres):
                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                test_result = "PASS"
                                delta_time = 601
                            elif(video_result_1 >= NOS_API.thres or video_result_2 >= NOS_API.thres):
                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                NOS_API.test_cases_results_info.inst_act_state = True
                                test_result = "PASS"
                                delta_time = 601                               
                            else: 
                                time.sleep(2)
                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                    video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                    if (video_result >= NOS_API.thres):
                                        result = 0
                                        while(result == 0):
                                            time.sleep(2)
                                            result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref"], 5, ["[FULL_SCREEN]"], [NOS_API.thres])
                                            NOS_API.test_cases_results_info.DidUpgrade = 1
                                        time.sleep(1)
                                        if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                        video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                        video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        if(video_result >= NOS_API.thres):
                                            time.sleep(60)   
                                            if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                            video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                            video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                            video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        if (video_result_2 >= NOS_API.thres or video_result_3 >= NOS_API.thres or video_result_4 >= NOS_API.thres):
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                            NOS_API.set_error_message("Não Actualiza") 
                                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                                if not(NOS_API.grab_picture("Check_Error")):
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
                                video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Check_Error", "[Upgrade_Error]");
                                video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Check_Error", "[Upgrade_Error]");
                                video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                if (video_result_2 >= NOS_API.thres or video_result_3 >= NOS_API.thres or video_result_4 >= NOS_API.thres):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                                TEST_CREATION_API.send_ir_rc_command("[UP]")
                                if(NOS_API.grab_picture("Channel")):
                                    video_result_0 = NOS_API.compare_pictures("black_720_ref", "Channel");
                                    if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        video_result_1 = NOS_API.mask_and_compare_pictures("Banner_720_ref", "Channel", "Banner_720_MASK")
                                        video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_720_ref", "Channel", "Banner_720_MASK")
                                        video_result_3 = NOS_API.mask_and_compare_pictures("Banner_720_ref2", "Channel", "Banner_720_MASK")
                                        if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                            delta_time = 601 
                                        else:
                                            time.sleep(0.2)
                                            counter = counter + 1                                            
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(0.2)
                                        counter = counter + 1
                                        delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                        
                    elif (video_height == "576" and counter < 4):
                        time.sleep(2)
                        if (NOS_API.grab_picture("Sw_Upgrade")):
                            video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                            if (video_result >= NOS_API.thres):
                                result = 0
                                while(result == 0):
                                    time.sleep(2)
                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_576"], 5, ["[FULL_SCREEN_576]"], [40])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                #video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                if(video_result >= NOS_API.thres):
                                    time.sleep(60) 
                                    if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                    #video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                    #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                #if (video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                #    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                #                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                #    NOS_API.set_error_message("Não Actualiza") 
                                #    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                #    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                #    test_result = "FAIL"
                                #    NOS_API.add_test_case_result_to_file_report(
                                #                    test_result,
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    error_codes,
                                #                    error_messages)
                                #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                #    report_file = ""    
                                #    if (test_result != "PASS"):
                                #        report_file = NOS_API.create_test_case_log_file(
                                #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                #                        NOS_API.test_cases_results_info.nos_sap_number,
                                #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                #                        "",
                                #                        end_time)
                                #        NOS_API.upload_file_report(report_file)
                                #        NOS_API.test_cases_results_info.isTestOK = False
                                #        
                                #        NOS_API.send_report_over_mqtt_test_plan(
                                #                test_result,
                                #                end_time,
                                #                error_codes,
                                #                report_file)
                                #    
                                #    
                                #    ## Update test result
                                #    TEST_CREATION_API.update_test_result(test_result)
                                #
                                #    ## Return DUT to initial state and de-initialize grabber device
                                #    NOS_API.deinitialize()
                                #    return
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        if(NOS_API.grab_picture("Channel")):
                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "Channel", "[FULL_SCREEN_576]");
                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_576_ref2", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    delta_time = 601 
                                else:
                                    time.sleep(0.2)
                                    counter = counter + 1                                    
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(0.2)
                                counter = counter + 1
                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                
                    elif (video_height == "1080" and counter < 4):
                        time.sleep(2)
                        if (NOS_API.grab_picture("Sw_Upgrade")):
                            video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                            if (video_result >= NOS_API.thres):
                                result = 0
                                while(result == 0):
                                    time.sleep(2)
                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_1080"], 5, ["[FULL_SCREEN_1080]"], [NOS_API.thres])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                if(video_result >= NOS_API.thres):
                                    time.sleep(60) 
                                    if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                    video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                    #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                if (video_result_2 >= NOS_API.thres):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                        if not(NOS_API.grab_picture("Check_Error")):
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
                        video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Check_Error", "[Upgrade_Error_1080]");
                        #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Check_Error", "[Upgrade_Error_1080]");
                        if (video_result_2 >= NOS_API.thres):
                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                            NOS_API.set_error_message("Não Actualiza") 
                            error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        if(NOS_API.grab_picture("Channel")):
                            video_result_0 = NOS_API.compare_pictures("black_1080_ref", "Channel", "[FULL_SCREEN_1080]");
                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_1080_ref2", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    delta_time = 601 
                                else: 
                                    time.sleep(0.2)
                                    counter = counter + 1        
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(0.2)
                                counter = counter + 1
                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))           
                    else:
                        delta_time = 602
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        break
                else:
                    NOS_API.grabber_stop_video_source()
                    ## Initialize input interfaces of DUT RT-AV101 device 
                    NOS_API.reset_dut()
                    time.sleep(2)
                    
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)

                    image_on_cvbs = False                    
                    if (NOS_API.is_signal_present_on_video_source()):
                        if(NOS_API.grab_picture("black_screen")):
                            video_result = NOS_API.compare_pictures("black_screen_cvbs", "black_screen");
                            if (video_result <= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                NOS_API.grabber_stop_video_source()
                                time.sleep(1)
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                time.sleep(1)
                                image_on_cvbs = True
                                if not(NOS_API.is_signal_present_on_video_source()):
                                    NOS_API.display_dialog("Verificar HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                    time.sleep(2)
                                if (NOS_API.is_signal_present_on_video_source()):
                                    time.sleep(3)
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                        time.sleep(45)
                                        continue
                                    if (video_height == "720" and counter < 4):
                                        if(NOS_API.grab_picture("boot_up_stage_hdmi")):
                                            video_result = NOS_API.mask_and_compare_pictures("installation_boot_up_ref", "boot_up_stage_hdmi", "File-MASK")
                                            video_result_0 = NOS_API.mask_and_compare_pictures("installation_boot_up_Eng_ref", "boot_up_stage_hdmi", "File-MASK_Eng")         
                                            video_result_1 = NOS_API.compare_pictures("No_Upgrade", "boot_up_stage_hdmi")
                                            video_result_2 = NOS_API.compare_pictures("No_Upgrade_1", "boot_up_stage_hdmi")
                                            if(video_result >= NOS_API.thres or video_result_0 >= NOS_API.thres):
                                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                                test_result = "PASS"
                                                delta_time = 601
                                            elif(video_result_1 >= NOS_API.thres or video_result_2 >= NOS_API.thres):
                                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                                NOS_API.test_cases_results_info.inst_act_state = True
                                                test_result = "PASS"
                                                delta_time = 601  
                                            else: 
                                                time.sleep(2)
                                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                                    video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                                    if (video_result >= NOS_API.thres):
                                                        result = 0
                                                        while(result == 0):
                                                            time.sleep(2)
                                                            result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref"], 5, ["[FULL_SCREEN]"], [NOS_API.thres])
                                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                                            video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                                            if(video_result >= NOS_API.thres):
                                                                time.sleep(60)            
                                                TEST_CREATION_API.send_ir_rc_command("[UP]")
                                                if(NOS_API.grab_picture("Channel")):
                                                    video_result_0 = NOS_API.compare_pictures("black_720_ref", "Channel");
                                                    if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                        video_result_1 = NOS_API.mask_and_compare_pictures("Banner_720_ref", "Channel", "Banner_720_MASK")
                                                        video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_720_ref", "Channel", "Banner_720_MASK")
                                                        video_result_3 = NOS_API.mask_and_compare_pictures("Banner_720_ref2", "Channel", "Banner_720_MASK")
                                                        if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                            delta_time = 601 
                                                        else:
                                                            time.sleep(0.2)
                                                            counter = counter + 1
                                                            image_on_cvbs = True
                                                    else:
                                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                        time.sleep(0.2)
                                                        counter = counter + 1
                                                        image_on_cvbs = True
                                                        delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                    elif (video_height == "576" and counter < 4):
                                        time.sleep(2)
                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                            video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                            if (video_result >= NOS_API.thres):
                                                result = 0
                                                while(result == 0):
                                                    time.sleep(2)
                                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_576"], 5, ["[FULL_SCREEN_576]"], [40])
                                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                                    video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                                    if(video_result >= NOS_API.thres):
                                                        time.sleep(60)
                                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                                        if(NOS_API.grab_picture("Channel")):
                                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "Channel", "[FULL_SCREEN_576]");
                                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_576_ref2", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                    delta_time = 601 
                                                else:
                                                    time.sleep(0.2)
                                                    counter = counter + 1
                                                    image_on_cvbs = True
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(0.2)
                                                counter = counter + 1
                                                image_on_cvbs = True
                                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                    elif (video_height == "1080" and counter < 4):    
                                        time.sleep(2)
                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                            video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                            if (video_result >= NOS_API.thres):
                                                result = 0
                                                while(result == 0):
                                                    time.sleep(2)
                                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_1080"], 5, ["[FULL_SCREEN_1080]"], [NOS_API.thres])
                                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                                    video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                                    if(video_result >= NOS_API.thres):
                                                        time.sleep(60)           
                                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                                        if(NOS_API.grab_picture("Channel")):
                                            video_result_0 = NOS_API.compare_pictures("black_1080_ref", "Channel", "[FULL_SCREEN_1080]");
                                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_1080_ref2", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                    delta_time = 601 
                                                else:
                                                    time.sleep(0.2)
                                                    counter = counter + 1
                                                    image_on_cvbs = True
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(0.2)
                                                counter = counter + 1
                                                image_on_cvbs = True
                                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                                    else:
                                        delta_time = 602
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                else:
                                    delta_time = 602
                                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                    error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                            else:
                                NOS_API.grabber_stop_video_source()
                                time.sleep(2)
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                time.sleep(0.2)
                                image_on_cvbs = True
                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                    if not (image_on_cvbs):
                        time.sleep(1)
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        time.sleep(1)
                        if (NOS_API.is_signal_present_on_video_source()):
                            time.sleep(3)
                            video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                            if (video_height != "576" and video_height != "720" and video_height != "1080"):
                                time.sleep(40)
                                continue
                            if (video_height == "720" and counter < 4):
                                if(NOS_API.grab_picture("boot_up_stage_hdmi")):            
                                    video_result = NOS_API.mask_and_compare_pictures("installation_boot_up_ref", "boot_up_stage_hdmi", "File-MASK")
                                    video_result_0 = NOS_API.mask_and_compare_pictures("installation_boot_up_Eng_ref", "boot_up_stage_hdmi", "File-MASK_Eng") 
                                    video_result_1 = NOS_API.compare_pictures("No_Upgrade", "boot_up_stage_hdmi") 
                                    video_result_2 = NOS_API.compare_pictures("No_Upgrade_1", "boot_up_stage_hdmi")
                                    if(video_result >= NOS_API.thres or video_result_0 >= NOS_API.thres):
                                        NOS_API.test_cases_results_info.channel_boot_up_state = False
                                        test_result = "PASS"
                                        delta_time = 601
                                    elif(video_result_1 >= NOS_API.thres or video_result_2 >= NOS_API.thres):
                                        NOS_API.test_cases_results_info.channel_boot_up_state = False
                                        NOS_API.test_cases_results_info.inst_act_state = True
                                        test_result = "PASS"
                                        delta_time = 601  
                                    else: 
                                        time.sleep(2)
                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                            video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                            if (video_result >= NOS_API.thres):
                                                result = 0
                                                while(result == 0):
                                                    time.sleep(2)
                                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref"], 5, ["[FULL_SCREEN]"], [NOS_API.thres])
                                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                                    video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade");
                                                    if(video_result >= NOS_API.thres):
                                                        time.sleep(60)      
                                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                                        if(NOS_API.grab_picture("Channel")):
                                            video_result_0 = NOS_API.compare_pictures("black_720_ref", "Channel");
                                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_720_ref", "Channel", "Banner_720_MASK")
                                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_720_ref", "Channel", "Banner_720_MASK")
                                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_720_ref2", "Channel", "Banner_720_MASK")
                                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                    delta_time = 601 
                                                else:
                                                    time.sleep(0.2)
                                                    counter = counter + 1                                                    
                                            else:
                                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(0.2)
                                                counter = counter + 1
                                                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))                    
                            elif (video_height == "576" and counter < 4):
                                time.sleep(2)
                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                    video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                    if (video_result >= NOS_API.thres):
                                        result = 0
                                        while(result == 0):
                                            time.sleep(2)
                                            result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_576"], 5, ["[FULL_SCREEN_576]"], [40])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                            video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                            if(video_result >= NOS_API.thres):
                                                time.sleep(60)
                                TEST_CREATION_API.send_ir_rc_command("[UP]")
                                if(NOS_API.grab_picture("Channel")):
                                    video_result_0 = NOS_API.compare_pictures("black_576_ref", "Channel", "[FULL_SCREEN_576]");
                                    if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        video_result_1 = NOS_API.mask_and_compare_pictures("Banner_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                        video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                        video_result_3 = NOS_API.mask_and_compare_pictures("Banner_576_ref2", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                        if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                            delta_time = 601 
                                        else:
                                            time.sleep(0.2)
                                            counter = counter + 1
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(0.2)
                                        counter = counter + 1
                                        delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))
                            elif (video_height == "1080" and counter < 4):   
                                time.sleep(2)
                                if (NOS_API.grab_picture("Sw_Upgrade")):
                                    video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                    if (video_result >= NOS_API.thres):
                                        result = 0
                                        while(result == 0):
                                            time.sleep(2)
                                            result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_1080"], 5, ["[FULL_SCREEN_1080]"], [NOS_API.thres])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                        if (NOS_API.grab_picture("Sw_Upgrade")):
                                            video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                            if(video_result >= NOS_API.thres):
                                                time.sleep(60) 
                                TEST_CREATION_API.send_ir_rc_command("[UP]")
                                if(NOS_API.grab_picture("Channel")):
                                    video_result_0 = NOS_API.compare_pictures("black_1080_ref", "Channel", "[FULL_SCREEN_1080]");
                                    if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        video_result_1 = NOS_API.mask_and_compare_pictures("Banner_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                        video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                        video_result_3 = NOS_API.mask_and_compare_pictures("Banner_1080_ref2", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                        if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                            delta_time = 601 
                                        else:
                                            time.sleep(0.2)
                                            counter = counter + 1     
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(0.2)
                                        counter = counter + 1
                                        delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))         
                            else:
                                delta_time = 602
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message )
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message                                                 
                        else:
                            time.sleep(1)
                            NOS_API.grabber_stop_video_source()
                            time.sleep(2)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            
                            delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))

            if(test_result == "FAIL" and delta_time != 602):     
                counter_1 = 0
                TEST_CREATION_API.send_ir_rc_command("[POWER_LESS]")
                result = NOS_API.wait_for_multiple_pictures(
                                ["Act_SSU", "Act_SSU_576", "Act_SSU_1080"],
                                15,
                                ["[Act_SSU]", "[Act_SSU_576]", "[Act_SSU_1080]"],
                                [80, 60, 80])
                if (result >= 0 and result < 3):
                    time.sleep(5)
                    NOS_API.test_cases_results_info.DidUpgrade = 1
                    if (NOS_API.wait_for_signal_sw_upgrade_thomson(350)):
                        time.sleep(2)
                    if (NOS_API.wait_for_signal_sw_upgrade_thomson(350)):
                        time.sleep(2)  
                        if (NOS_API.wait_for_signal_sw_upgrade_thomson(350)):
                            time.sleep(10) 
                if not(NOS_API.is_signal_present_on_video_source()):
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(8)
                time.sleep(1)
                if not(NOS_API.is_signal_present_on_video_source()):
                    NOS_API.grabber_stop_video_source()                                    
                    ## Initialize input interfaces of DUT RT-AV101 device 
                    NOS_API.reset_dut()
                    time.sleep(2)                                    
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)                                   
                    time.sleep(2)                                   
                    if (NOS_API.is_signal_present_on_video_source()):
                        if not(NOS_API.grab_picture("black")):
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
                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            time.sleep(4)
                        else:
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            time.sleep(4)
                            NOS_API.display_dialog("Verificar HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            time.sleep(2)
                            if not(NOS_API.is_signal_present_on_video_source()):
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
                
                    else:   
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        time.sleep(4)
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(8)
                time.sleep(1)
                if not(NOS_API.is_signal_present_on_video_source()):
                    NOS_API.grabber_stop_video_source()                                    
                    ## Initialize input interfaces of DUT RT-AV101 device 
                    NOS_API.reset_dut()
                    time.sleep(2)                                    
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)                                   
                    time.sleep(2)                                   
                    if (NOS_API.is_signal_present_on_video_source()):
                        if not(NOS_API.grab_picture("black")):
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
                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            time.sleep(4)
                        else:
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            time.sleep(4)
                            NOS_API.display_dialog("Verificar HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            time.sleep(2)
                            if not(NOS_API.is_signal_present_on_video_source()):
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
                
                    else:   
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        time.sleep(4)
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(8)
                time.sleep(1)
                if not(NOS_API.is_signal_present_on_video_source()):
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(8)
                time.sleep(1)
                if (NOS_API.is_signal_present_on_video_source()):
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height == "720"):
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        if not(NOS_API.grab_picture("black")):
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
                        video_result_0 = NOS_API.compare_pictures("black_720_ref", "black");
                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            NOS_API.grabber_stop_video_source()
                            NOS_API.reset_dut()
                            time.sleep(2)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            time.sleep(2)
                            if not(NOS_API.grab_picture("black")):
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
                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                            if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(5)
                                NOS_API.grabber_stop_video_source()
                                time.sleep(1)
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                time.sleep(8)
                    elif (video_height == "576"):
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        if not(NOS_API.grab_picture("black")):
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
                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            NOS_API.grabber_stop_video_source()
                            NOS_API.reset_dut()
                            time.sleep(2)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            time.sleep(2)
                            if not(NOS_API.grab_picture("black")):
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
                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                            if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(5)
                                NOS_API.grabber_stop_video_source()
                                time.sleep(1)
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                time.sleep(8)
                    elif(video_height == "1080"):
                        TEST_CREATION_API.send_ir_rc_command("[UP]")
                        if not(NOS_API.grab_picture("black")):
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
                        video_result_0 = NOS_API.compare_pictures("black_1080_ref", "black", "[FULL_SCREEN_1080]");
                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            NOS_API.grabber_stop_video_source()
                            NOS_API.reset_dut()
                            time.sleep(2)
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                            time.sleep(2)
                            if not(NOS_API.grab_picture("black")):
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
                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_1080]");
                            if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(3)
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                time.sleep(5)
                                NOS_API.grabber_stop_video_source()
                                time.sleep(1)
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                time.sleep(8)
                while (counter_1 < 3):
                    if (NOS_API.is_signal_present_on_video_source()):
                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height != "576" and video_height != "720" and video_height != "1080"):
                            time.sleep(40)
                            continue
                        if (video_height == "720"):
                            if not(NOS_API.grab_picture("boot_up_stage_hdmi")):
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
                            video_result = NOS_API.mask_and_compare_pictures("installation_boot_up_ref", "boot_up_stage_hdmi", "File-MASK")
                            video_result_0 = NOS_API.mask_and_compare_pictures("installation_boot_up_Eng_ref", "boot_up_stage_hdmi", "File-MASK_Eng")  
                            video_result_1 = NOS_API.compare_pictures("No_Upgrade", "boot_up_stage_hdmi")
                            video_result_2 = NOS_API.compare_pictures("No_Upgrade_1", "boot_up_stage_hdmi")
                            if(video_result >= NOS_API.thres or video_result_0 >= NOS_API.thres):       
                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                test_result = "PASS"
                                delta_time = 601
                                break
                            elif(video_result_1 >= NOS_API.thres or video_result_2 >= NOS_API.thres):
                                NOS_API.test_cases_results_info.channel_boot_up_state = False
                                NOS_API.test_cases_results_info.inst_act_state = True
                                test_result = "PASS"
                                delta_time = 601  
                                break
                            else: 
                                time.sleep(3)  
                                if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade")
                                video_result_1 = NOS_API.compare_pictures("No_Upgrade", "Sw_Upgrade")
                                video_result_2 = NOS_API.compare_pictures("No_Upgrade_1", "Sw_Upgrade")
                                if (video_result >= NOS_API.thres):
                                    result = 0
                                    while(result == 0):
                                        time.sleep(2)
                                        result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref"], 5, ["[FULL_SCREEN]"], [NOS_API.thres])
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                    time.sleep(1)
                                    if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                    video_result = NOS_API.compare_pictures("Upgrade_ref", "Sw_Upgrade")
                                    video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]")
                                    video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]")
                                    video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]")
                                    if(video_result >= NOS_API.thres):
                                        time.sleep(60)
                                        if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                        video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                        video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                    if (video_result_2 >= NOS_API.thres or video_result_3 >= NOS_API.thres or video_result_4 >= NOS_API.thres):
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                        NOS_API.set_error_message("Não Actualiza") 
                                        error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                                elif(video_result_1 >= NOS_API.thres or video_result_2 >= NOS_API.thres):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = False
                                    NOS_API.test_cases_results_info.inst_act_state = True
                                    test_result = "PASS"
                                    delta_time = 601
                                    break
                            if not(NOS_API.grab_picture("Check_Error")):
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
                            video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Check_Error", "[Upgrade_Error]");
                            video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Check_Error", "[Upgrade_Error]");
                            video_result_4 = NOS_API.compare_pictures("Upgrade_Error2_ref", "Sw_Upgrade", "[Upgrade_Error]");
                            if (video_result_2 >= NOS_API.thres or video_result_3 >= NOS_API.thres or video_result_4 >= NOS_API.thres):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                            video_result_0 = NOS_API.compare_pictures("black_720_ref", "Channel")
                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_720_ref", "Channel", "Banner_720_MASK")
                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_720_ref", "Channel", "Banner_720_MASK")
                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_720_ref2", "Channel", "Banner_720_MASK")
                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True      
                                    test_result = "PASS"
                                    delta_time = 601
                                    break
                                else:
                                    if (counter_1 == 2):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                        counter_1 = 3
                                    else:
                                        NOS_API.grabber_stop_video_source()
                                        #NOS_API.reset_dut()
                                        time.sleep(2)
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        time.sleep(0.2)
                                        counter_1 = counter_1 + 1 
                            else:
                                if (counter_1 == 2):
                                    NOS_API.grabber_stop_video_source()                                    
                                    ## Initialize input interfaces of DUT RT-AV101 device 
                                    NOS_API.reset_dut()
                                    time.sleep(2)                                    
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)                                   
                                    time.sleep(2)                                   
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        if not(NOS_API.grab_picture("black")):
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
                                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.write_log_to_file("No boot")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                            NOS_API.set_error_message("Não arranca")
                                            error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                            counter_1 = 3
                                        else:
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                                            counter_1 = 3
                                    else:
                                        TEST_CREATION_API.write_log_to_file("No boot")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                        NOS_API.set_error_message("Não arranca")
                                        error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                        error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                        counter_1 = 3
                                else:
                                    NOS_API.grabber_stop_video_source()
                                    #NOS_API.reset_dut()
                                    time.sleep(2)
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                    time.sleep(0.2)
                                    counter_1 = counter_1 + 1              
                        elif (video_height == "576"):
                            time.sleep(3)
                            if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                            video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                            if (video_result >= NOS_API.thres):
                                result = 0
                                while(result == 0):
                                    time.sleep(2)
                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_576"], 5, ["[FULL_SCREEN_576]"], [40])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                time.sleep(1)
                                if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                video_result = NOS_API.compare_pictures("Upgrade_ref_576", "Sw_Upgrade");
                                #video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                if(video_result >= NOS_API.thres):
                                    time.sleep(60)
                                    if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                    #video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                    #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error]");
                                #if (video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                #    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                #                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                #    NOS_API.set_error_message("Não Actualiza") 
                                #    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                #    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                #    test_result = "FAIL"
                                #    NOS_API.add_test_case_result_to_file_report(
                                #                    test_result,
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    "- - - - - - - - - - - - - - - - - - - -",
                                #                    error_codes,
                                #                    error_messages)
                                #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                #    report_file = ""    
                                #    if (test_result != "PASS"):
                                #        report_file = NOS_API.create_test_case_log_file(
                                #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                #                        NOS_API.test_cases_results_info.nos_sap_number,
                                #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                #                        "",
                                #                        end_time)
                                #        NOS_API.upload_file_report(report_file)
                                #        NOS_API.test_cases_results_info.isTestOK = False
                                #        
                                #        NOS_API.send_report_over_mqtt_test_plan(
                                #                test_result,
                                #                end_time,
                                #                error_codes,
                                #                report_file)
                                #    
                                #    
                                #    ## Update test result
                                #    TEST_CREATION_API.update_test_result(test_result)
                                #
                                #    ## Return DUT to initial state and de-initialize grabber device
                                #    NOS_API.deinitialize()
                                #    return
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
                            video_result_0 = NOS_API.compare_pictures("black_576_ref", "Channel", "[FULL_SCREEN_576]");
                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_576_ref", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_576_ref2", "Channel", "Banner_576_MASK", TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_576]")
                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True      
                                    test_result = "PASS"
                                    delta_time = 601
                                    break
                                else:
                                    if (counter_1 == 2):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_576p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_576p_noise_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_576p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_576p_noise_error_message
                                        counter_1 = 3
                                    else:
                                        NOS_API.grabber_stop_video_source()
                                        #NOS_API.reset_dut()
                                        time.sleep(2)
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        time.sleep(0.2)
                                        counter_1 = counter_1 + 1 
                            else:
                                if (counter_1 == 2):
                                    NOS_API.grabber_stop_video_source()                                    
                                    ## Initialize input interfaces of DUT RT-AV101 device 
                                    NOS_API.reset_dut()
                                    time.sleep(2)                                    
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)                                   
                                    time.sleep(2)                                   
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        if not(NOS_API.grab_picture("black")):
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
                                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.write_log_to_file("No boot")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                            NOS_API.set_error_message("Não arranca")
                                            error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                            counter_1 = 3
                                        else:
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_576p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_576p_noise_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.hdmi_576p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_576p_noise_error_message
                                            counter_1 = 3
                                    else:
                                        TEST_CREATION_API.write_log_to_file("No boot")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                        NOS_API.set_error_message("Não arranca")
                                        error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                        error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                        counter_1 = 3
                                else:
                                    NOS_API.grabber_stop_video_source()
                                    #NOS_API.reset_dut()
                                    time.sleep(2)
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                    time.sleep(0.2)
                                    counter_1 = counter_1 + 1 
                        elif (video_height == "1080"):    
                            time.sleep(3)
                            if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                            video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                            if (video_result >= NOS_API.thres):
                                result = 0
                                while(result == 0):
                                    time.sleep(2)
                                    result = NOS_API.wait_for_multiple_pictures(["Upgrade_ref_1080"], 5, ["[FULL_SCREEN_1080]"], [NOS_API.thres])
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                video_result = NOS_API.compare_pictures("Upgrade_ref_1080", "Sw_Upgrade");
                                video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                if(video_result >= NOS_API.thres):
                                    time.sleep(60)
                                    if not(NOS_API.grab_picture("Sw_Upgrade")):
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
                                    video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                    #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Sw_Upgrade", "[Upgrade_Error_1080]");
                                if (video_result_2 >= NOS_API.thres):
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                            if not(NOS_API.grab_picture("Check_Error")):
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
                            video_result_2 = NOS_API.compare_pictures("Upgrade_Error6_1080_ref", "Check_Error", "[Upgrade_Error_1080]");
                            #video_result_3 = NOS_API.compare_pictures("Upgrade_Error3_ref", "Check_Error", "[Upgrade_Error_1080]");
                            if (video_result_2 >= NOS_API.thres):
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
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
                            video_result_0 = NOS_API.compare_pictures("black_1080_ref", "Channel", "[FULL_SCREEN_1080]");
                            if (video_result_0 <= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                video_result_1 = NOS_API.mask_and_compare_pictures("Banner_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                video_result_2 = NOS_API.mask_and_compare_pictures("Banner_Eng_1080_ref", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                video_result_3 = NOS_API.mask_and_compare_pictures("Banner_1080_ref2", "Channel", "Banner_1080_MASK",TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD,"[FULL_SCREEN_1080]")
                                if(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_2 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_3 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True      
                                    test_result = "PASS"
                                    delta_time = 601
                                    break
                                else:
                                    if (counter_1 == 2):
                                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                        counter_1 = 3
                                    else:
                                        NOS_API.grabber_stop_video_source()
                                        #NOS_API.reset_dut()
                                        time.sleep(2)
                                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                        time.sleep(0.2)
                                        counter_1 = counter_1 + 1
                            else:   
                                if (counter_1 == 2):
                                    NOS_API.grabber_stop_video_source()                                    
                                    ## Initialize input interfaces of DUT RT-AV101 device 
                                    NOS_API.reset_dut()
                                    time.sleep(2)                                    
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)                                   
                                    time.sleep(2)                                   
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        if not(NOS_API.grab_picture("black")):
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
                                        video_result_0 = NOS_API.compare_pictures("black_576_ref", "black", "[FULL_SCREEN_576]");
                                        if (video_result_0 > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                            TEST_CREATION_API.write_log_to_file("No boot")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                            NOS_API.set_error_message("Não arranca")
                                            error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                            counter_1 = 3
                                        else:
                                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                            counter_1 = 3
                                    else:
                                        TEST_CREATION_API.write_log_to_file("No boot")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                        NOS_API.set_error_message("Não arranca")
                                        error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                        error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                        counter_1 = 3
                                else:
                                    NOS_API.grabber_stop_video_source()
                                    time.sleep(2)
                                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                    time.sleep(0.2)
                                    counter_1 = counter_1 + 1
                        else:
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                        
                    else:
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        ## Initialize input interfaces of DUT RT-AV101 device 
                        NOS_API.reset_dut()
                        time.sleep(2)
                            
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)
                        time.sleep(1)
                        counter_1 = 3
                        if (NOS_API.is_signal_present_on_video_source()):
                            time.sleep(2)
                            if not(NOS_API.grab_picture("black_screen")):
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
                            video_result = NOS_API.compare_pictures("black_screen_cvbs", "black_screen");
                            if (video_result <= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_noise_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_noise_error_message
                            else:
                                #delta_time = 62
                                TEST_CREATION_API.write_log_to_file("No boot")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                NOS_API.set_error_message("Não arranca")
                                error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                        else:   
                            TEST_CREATION_API.write_log_to_file("No boot")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                            NOS_API.set_error_message("Não arranca")
                            error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                            error_messages = NOS_API.test_cases_results_info.no_boot_error_message    
                
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
   