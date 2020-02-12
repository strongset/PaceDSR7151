# Test name = Zap Test
# Test description = Check image and audio after channel up/channel down
from datetime import datetime
import time
import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

## Max record audio time in miliseconds
MAX_RECORD_AUDIO_TIME = 2000
MAX_RECORD_VIDEO_TIME = 3000

def runTest():
    System_Failure = 0
    while(System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            pqm_analyse_check = True
            
            error_codes = ""
            error_messages = ""
            
            NOS_API.test_cases_results_info.chUp_state = False
            
            chUp_counter = 0
            chDown_counter = 0
            counter = 0
            
            ZAP_Result = False
            HDMI_1080i_Result = False
            test_result_res = False
            test_result_output = False
            SCART_Result = False
            test_result_SCART_video = False
            SPDIF_test = False
            test_result_ButtonLeds = False
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()
            
            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
            
            if(System_Failure == 1):
                TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                if (NOS_API.is_signal_present_on_video_source()):
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "720"):
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p]")
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p_1]")
                        time.sleep(2)
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
            
                        TEST_CREATION_API.send_ir_rc_command("[Exit_Menu]")
                        
            if (NOS_API.is_signal_present_on_video_source()):
                ## Set volume to max
                TEST_CREATION_API.send_ir_rc_command("[VOL_MAX]")
        
                ## Zap to service
                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                time.sleep(2)            
                    
                while (chUp_counter < 3):                    
                    #if (chUp_counter == 2):
                    #    try:
                    #        ## Return DUT to initial state and de-initialize grabber device
                    #        NOS_API.deinitialize()
                    #    except: 
                    #        pass
                    #        
                    #    NOS_API.Inspection = True
                    #    
                    #    if (NOS_API.configure_power_switch_by_inspection()):
                    #        if not(NOS_API.power_off()): 
                    #            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                    #            ## Update test result
                    #            TEST_CREATION_API.update_test_result(test_result)
                    #            NOS_API.set_error_message("Inspection")
                    #            
                    #            NOS_API.add_test_case_result_to_file_report(
                    #                            test_result,
                    #                            "- - - - - - - - - - - - - - - - - - - -",
                    #                            "- - - - - - - - - - - - - - - - - - - -",
                    #                            error_codes,
                    #                            error_messages)
                    #            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                    #            report_file = ""
                    #            if (test_result != "PASS"):
                    #                report_file = NOS_API.create_test_case_log_file(
                    #                                NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                                NOS_API.test_cases_results_info.nos_sap_number,
                    #                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                                "",
                    #                                end_time)
                    #                NOS_API.upload_file_report(report_file)
                    #                NOS_API.test_cases_results_info.isTestOK = False
                    #            
                    #            
                    #            ## Update test result
                    #            TEST_CREATION_API.update_test_result(test_result)
                    #        
                    #            ## Return DUT to initial state and de-initialize grabber device
                    #            NOS_API.deinitialize()
                    #            
                    #            NOS_API.send_report_over_mqtt_test_plan(
                    #                        test_result,
                    #                        end_time,
                    #                        error_codes,
                    #                        report_file)
                    #
                    #            return
                    #        time.sleep(10)
                    #        ## Power on STB with energenie
                    #        if not(NOS_API.power_on()):
                    #            TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                    #            ## Update test result
                    #            TEST_CREATION_API.update_test_result(test_result)
                    #            NOS_API.set_error_message("Inspection")
                    #            
                    #            NOS_API.add_test_case_result_to_file_report(
                    #                            test_result,
                    #                            "- - - - - - - - - - - - - - - - - - - -",
                    #                            "- - - - - - - - - - - - - - - - - - - -",
                    #                            error_codes,
                    #                            error_messages)
                    #            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                    #            report_file = ""
                    #            if (test_result != "PASS"):
                    #                report_file = NOS_API.create_test_case_log_file(
                    #                                NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                                NOS_API.test_cases_results_info.nos_sap_number,
                    #                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                                "",
                    #                                end_time)
                    #                NOS_API.upload_file_report(report_file)
                    #                NOS_API.test_cases_results_info.isTestOK = False
                    #            
                    #            test_result = "FAIL"
                    #            
                    #            ## Update test result
                    #            TEST_CREATION_API.update_test_result(test_result)
                    #        
                    #            ## Return DUT to initial state and de-initialize grabber device
                    #            NOS_API.deinitialize()
                    #            
                    #            NOS_API.send_report_over_mqtt_test_plan(
                    #                    test_result,
                    #                    end_time,
                    #                    error_codes,
                    #                    report_file)
                    #            
                    #            return
                    #        time.sleep(15)
                    #    else:
                    #        TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    #        
                    #        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                    #                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    #        NOS_API.set_error_message("Inspection")
                    #        
                    #        NOS_API.add_test_case_result_to_file_report(
                    #                        test_result,
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        error_codes,
                    #                        error_messages)
                    #        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    #        report_file = ""
                    #        if (test_result != "PASS"):
                    #            report_file = NOS_API.create_test_case_log_file(
                    #                            NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                            NOS_API.test_cases_results_info.nos_sap_number,
                    #                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                            "",
                    #                            end_time)
                    #            NOS_API.upload_file_report(report_file)
                    #            NOS_API.test_cases_results_info.isTestOK = False
                    #        
                    #        test_result = "FAIL"
                    #        ## Update test result
                    #        TEST_CREATION_API.update_test_result(test_result)
                    #        
                    #    
                    #        ## Return DUT to initial state and de-initialize grabber device
                    #        NOS_API.deinitialize()
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #            test_result,
                    #            end_time,
                    #            error_codes,
                    #            report_file)
                    #        
                    #        return
                    #    
                    #    NOS_API.Inspection = False
                    #    
                    #    NOS_API.initialize_grabber()
                    #    
                    #    ## Start grabber device with video on default video source
                    #    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                    #    TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                    #    time.sleep(2)  
                    
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    
                    ## Perform grab picture
                    if not(NOS_API.grab_picture("service_2")):
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
                    video_result = NOS_API.compare_pictures("service_2_ref", "service_2", "[HALF_SCREEN]")
                    video_result_1 = NOS_API.compare_pictures("service_2_ref_2", "service_2", "[HALF_SCREEN]")
                    ## Check if STB zap to horizontal polarization channel (check image and audio)
                    if ((video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD) or (video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD)):                  
                        # Record audio from HDMI
                        TEST_CREATION_API.record_audio("audio_chUp", MAX_RECORD_AUDIO_TIME)
                        
                        #Amostra sem som
                        audio_result_1 = NOS_API.compare_audio("No_Both_ref", "audio_chUp")
                        
                        if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):                              

                            NOS_API.test_cases_results_info.chUp_state = True
                            break   
                        else:
                            if (chUp_counter == 2):
                                TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                NOS_API.set_error_message("Audio HDMI")
                                NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                chUp_counter = 3                           
                            else:                      
                                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                                time.sleep(2)
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                chUp_counter = chUp_counter + 1
                    else:
                        if (chUp_counter == 2):
                            TEST_CREATION_API.write_log_to_file("STB is not zap to service 2 (ChUp failed)")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.zap_channel_up_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_up_error_message )
                            NOS_API.set_error_message("Tuner")
                            error_codes = NOS_API.test_cases_results_info.zap_channel_up_error_code
                            error_messages = NOS_API.test_cases_results_info.zap_channel_up_error_message
                            chUp_counter = 3
                        else:
                            if (chUp_counter == 0):
                                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                                TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                chUp_counter = chUp_counter + 1
                            else:
                                chUp_counter = chUp_counter + 1
                ###################
                ## CH Down
                ###################
                if (NOS_API.test_cases_results_info.chUp_state):
                    
                    TEST_CREATION_API.send_ir_rc_command("[CH_3]")   

                    time.sleep(2)
                    
                    if not (NOS_API.is_signal_present_on_video_source()):
                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        NOS_API.set_error_message("Reboot")
                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
                        test_result = "FAIL"
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                        
                        
                    ## Record video with duration of recording (10 seconds)
                    NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
            
                    ## Instance of PQMAnalyse type
                    pqm_analyse = TEST_CREATION_API.PQMAnalyse()
            
                    ## Set what algorithms should be checked while analyzing given video file with PQM.
                    # Attributes are set to false by default.
                    pqm_analyse.black_screen_activ = True
                    pqm_analyse.blocking_activ = True
                    pqm_analyse.freezing_activ = True
            
                    # Name of the video file that will be analysed by PQM.
                    pqm_analyse.file_name = "video"
            
                    ## Analyse recorded video
                    analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
            
                    if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.set_error_message("Video HDMI")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code)
                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
                    if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.set_error_message("Video HDMI")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                            
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                    if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.set_error_message("Video HDMI")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                    
                    if not(pqm_analyse_check): 
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                    
                    if not(analysed_video): 
                        if(System_Failure == 0):
                            System_Failure = System_Failure + 1 
                            NOS_API.Inspection = True
                            if(System_Failure == 1):
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
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
                                continue
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
                            TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                            error_codes = NOS_API.test_cases_results_info.grabber_error_code
                            error_messages = NOS_API.test_cases_results_info.grabber_error_message
                            NOS_API.set_error_message("Inspection")
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                      
                    if (NOS_API.is_video_playing):
                        while (chDown_counter < 3):
                            if (chDown_counter == 2):
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                except: 
                                    pass
                                    
                                NOS_API.Inspection = True
                                
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
                                    time.sleep(15)
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
                                
                                NOS_API.initialize_grabber()
                                
                                ## Start grabber device with video on default video source
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)
                                time.sleep(2) 
                                
                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                            
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("service_1")):
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
                            video_result = NOS_API.compare_pictures("service_1_ref", "service_1", "[HALF_SCREEN]")
            
                            ## Check if STB zap to horizontal polarization channel (check image and audio)
                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
            
                                ## Record audio from HDMI
                                TEST_CREATION_API.record_audio("audio_chDown", MAX_RECORD_AUDIO_TIME)

                                #Amostra sem som
                                audio_result_1 = NOS_API.compare_audio("No_Both_ref", "audio_chDown")
                                
                                #if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):                            
                                    ZAP_Result = True
                                    break
                                            
                                else:
                                    if (chDown_counter == 2):
                                        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                        NOS_API.set_error_message("Audio HDMI")
                                        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                        chUp_counter = 3 
                                    else:                        
                                        TEST_CREATION_API.send_ir_rc_command("[CH_3]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                        TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                        chDown_counter = chDown_counter + 1
                            else:
                                if (chDown_counter == 2):
                                    TEST_CREATION_API.write_log_to_file("STB is not zap to service 1")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.zap_channel_down_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_down_error_message)
                                    NOS_API.set_error_message("Tuner")
                                    error_codes = NOS_API.test_cases_results_info.zap_channel_down_error_code
                                    error_messages = NOS_API.test_cases_results_info.zap_channel_down_error_message
                                    chDown_counter = 3
                                else:                        
                                    TEST_CREATION_API.send_ir_rc_command("[CH_3]")
                                    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                                    chDown_counter = chDown_counter + 1
            else:
                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                NOS_API.set_error_message("Video HDMI")    
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
             
    ########################################################################################### 1080i HDMI Test ########################################################################################################################
   
            if(ZAP_Result):
                 
                ############################################### Set Resolution 1080p ########################################################            
                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p]")
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height != "1080"):
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p]")
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height != "1080"):
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message)
                    error_codes = NOS_API.test_cases_results_info.resolution_error_code
                    error_messages = NOS_API.test_cases_results_info.resolution_error_message
                    NOS_API.set_error_message("Resolução")
                else:
                    test_result_res = True
                    
    ######################################################################################### 1080p HDMI Video Output##################################################################################################################
                
                if(test_result_res):
                    TEST_CREATION_API.send_ir_rc_command("[Left]")
                    TEST_CREATION_API.send_ir_rc_command("[Left]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    
                    if not(NOS_API.is_signal_present_on_video_source()):
                        time.sleep(5)
                    if (NOS_API.is_signal_present_on_video_source()):
            
                        ## Record video with duration of recording (10 seconds)
                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                
                        ## Instance of PQMAnalyse type
                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                
                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                        # Attributes are set to false by default.
                        pqm_analyse.black_screen_activ = True
                        pqm_analyse.blocking_activ = True
                        pqm_analyse.freezing_activ = True
                
                        # Name of the video file that will be analysed by PQM.
                        pqm_analyse.file_name = "video"
                
                        ## Analyse recorded video
                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                
                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            NOS_API.set_error_message("Video HDMI")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message
                            
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
                            
                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            NOS_API.set_error_message("Video HDMI")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                                
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                                
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
                            
                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            NOS_API.set_error_message("Video HDMI")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                            
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                                
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
                            
                        if (analysed_video):            
                            test_result_output = True
                        else:
                            if(System_Failure == 0):
                                System_Failure = System_Failure + 1 
                                NOS_API.Inspection = True
                                if(System_Failure == 1):
                                    try:
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
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
                                    continue
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
                                TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                                NOS_API.set_error_message("Inspection")
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                        NOS_API.set_error_message("Video HDMI")
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                ################################################## 1080p HDMI Video Quality ############################################################
                    
                if(test_result_output):
                            
                    counter = 0
                    video_result = 0
                    while (counter < 3):
                        ## Perform grab picture
                        if not(NOS_API.grab_picture("HDMI_video")):
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
                        ## Compare grabbed and expected image and get result of comparison
                        video_result = NOS_API.compare_pictures("HDMI_video_ref", "HDMI_video", "[HALF_SCREEN_1080p]")

                        ## Check video analysis results and update comments
                        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            ## Set test result to PASS
                            HDMI_1080i_Result = True
                            TEST_CREATION_API.write_log_to_file("Video Result: "+str(video_result))
                            TEST_CREATION_API.write_log_to_file("Video THRESHOLD: "+str(TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD))
                            break
                        else:
                            NOS_API.set_error_message("Video HDMI")
                            TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 1080p.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message)
                            TEST_CREATION_API.write_log_to_file("Video Result: "+str(video_result))
                            TEST_CREATION_API.write_log_to_file("Video THRESHOLD: "+str(TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD))
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message                   
                              
    ################################################################################################## SCART Test ######################################################################################################################
                  
                if(HDMI_1080i_Result):
                    
                    TEST_CREATION_API.grabber_stop_video_source()
                    time.sleep(1)
                    TEST_CREATION_API.grabber_stop_audio_source()
                    time.sleep(1)
                 
                    ## Initialize input interfaces of DUT RT-AV101 device 
                    NOS_API.reset_dut()

                    ## Start grabber device with video on default video source
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS2)

                    if not(NOS_API.is_signal_present_on_video_source()):
                        NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                    
                    #TEST_CREATION_API.send_ir_rc_command("[VOL HALF]")
                    
                    if (NOS_API.is_signal_present_on_video_source()):
                        ## Check if video is playing (check if video is not freezed)
                        if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS2)):
                            video_result = 0
                            counter = 0
                            try:    
                                ## Perform grab picture
                                if not(NOS_API.grab_picture("SCART_video")):
                                    TEST_CREATION_API.write_log_to_file("No Signal on Scart")
                                    NOS_API.set_error_message("Video Scart")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                    
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
                                ## Compare grabbed and expected image and get result of comparison
                                video_result = NOS_API.compare_pictures("SCART_video_ref", "SCART_video", "[HALF_SCREEN_576p]")
                                
                            except Exception as error:
                                ## Set test result to INCONCLUSIVE
                                TEST_CREATION_API.write_log_to_file(str(error))
                                test_result = "FAIL"
                                TEST_CREATION_API.write_log_to_file("There is no signal on SCART interface.")
                                
                            ## Check video analysis results and update comments
                            if (video_result >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                ## Set test result to PASS
                                test_result_SCART_video = True
                                TEST_CREATION_API.write_log_to_file("Video Result: "+str(video_result))
                                TEST_CREATION_API.write_log_to_file("Video THRESHOLD: "+str(NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD))
                            else:
                                TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on SCART interface.")
                                NOS_API.set_error_message("Video Scart")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_noise_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_noise_error_message)
                                TEST_CREATION_API.write_log_to_file("Video Result: "+str(video_result))
                                TEST_CREATION_API.write_log_to_file("Video THRESHOLD: "+str(NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD))
                                error_codes = NOS_API.test_cases_results_info.scart_noise_error_code
                                error_messages =  NOS_API.test_cases_results_info.scart_noise_error_message
                
                        else:
                            TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on SCART interface.")
                            NOS_API.set_error_message("Video Scart")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_freezing_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.scart_image_freezing_error_message \
                                                                + "; Video is not playing on SCART interface")
                            error_codes = NOS_API.test_cases_results_info.scart_image_freezing_error_code
                            error_messages = NOS_API.test_cases_results_info.scart_image_freezing_error_message
                    else:
                        TEST_CREATION_API.write_log_to_file("No Signal on Scart")
                        NOS_API.set_error_message("Video Scart")
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                        error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                        error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                        
    ################################################################################################## SCART Audio ######################################################################################################################                    

                    if(test_result_SCART_video):
                    
                        TEST_CREATION_API.grabber_stop_video_source()
                        time.sleep(0.5)
                        
                        ## Start grabber device with audio on SCART audio source
                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                        time.sleep(3)
                
                        Audio_Counter = 0

                        while (Audio_Counter < 3):
                        
                            if (Audio_Counter == 1):
                                NOS_API.display_dialog("Confirme o cabo SCART e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            if (Audio_Counter == 2):
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                except: 
                                    pass
                                    
                                NOS_API.Inspection = True
                                
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
                                    time.sleep(15)
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
                                
                                NOS_API.initialize_grabber()
                                
                                ## Start grabber device with audio on SCART audio source
                                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN2)
                                time.sleep(3)
                            
                            ## Record audio from digital output (SCART)
                            TEST_CREATION_API.record_audio("SCART_audio", MAX_RECORD_AUDIO_TIME)

                    #############Comparacao com referencia audio NOK############################################
                                
                            ## Compare recorded and expected audio and get result of comparison
                            audio_result_1 = NOS_API.compare_audio("No_Left_ref", "SCART_audio")
                            audio_result_2 = NOS_API.compare_audio("No_right_ref", "SCART_audio")
                            audio_result_3 = NOS_API.compare_audio("No_Both_ref", "SCART_audio")
                            
                            ## Check is audio present on channel
                            if (TEST_CREATION_API.is_audio_present("SCART_audio")):
                                if not(audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_3 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                    SCART_Result = True
                                    break
                                else:
                                    if (Audio_Counter == 2):
                                        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SCART interface.")
                                        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code  \
                                                                                    + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_code  \
                                                                                    + "; Error messages: " + NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message \
                                                                                    + ";\n" + NOS_API.test_cases_results_info.scart_signal_interference_error_message)
                                        error_codes = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_code
                                        error_messages = NOS_API.test_cases_results_info.scart_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.scart_signal_interference_error_message
                                        NOS_API.set_error_message("Audio Scart") 
                                        Audio_Counter = 3
                                    else:        
                                        Audio_Counter = Audio_Counter + 1                
                            else:
                                if (Audio_Counter == 2):
                                    TEST_CREATION_API.write_log_to_file("Audio is not present on SCART interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_signal_absence_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.scart_signal_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.scart_signal_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.scart_signal_absence_error_message
                                    NOS_API.set_error_message("Audio Scart") 
                                    Audio_Counter = 3
                                else:
                                    Audio_Counter = Audio_Counter + 1
                   
    ################################################################################################## SPDIF Test ######################################################################################################################        
                        
                    if(SCART_Result):
                    
                        TEST_CREATION_API.grabber_stop_audio_source()
                        time.sleep(1)        
                        
                        ## Start grabber device with audio on SPDIF Coaxial source
                        TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_COAX)
                        time.sleep(2)

                        Audio_Counter = 0
                        
                        while (Audio_Counter < 3):

                            if (Audio_Counter == 1):
                                NOS_API.display_dialog("Confirme o cabo SPDIF e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"                           
                            if (Audio_Counter == 2):
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                except: 
                                    pass
                                    
                                NOS_API.Inspection = True
                                
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
                                    time.sleep(15)
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
                                
                                NOS_API.initialize_grabber()
                                
                                ## Start grabber device with audio on SPDIF Coaxial source
                                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.SPDIF_COAX)
                                time.sleep(3)
                                
                            ## Record audio from digital output (SPDIF COAX)
                            TEST_CREATION_API.record_audio("SPDIF_COAX_audio", MAX_RECORD_AUDIO_TIME)
                            
                            #Amostra sem som
                            audio_result_1 = NOS_API.compare_audio("No_Both_ref", "SPDIF_COAX_audio")

                            ## Check is audio present on channel
                            if (TEST_CREATION_API.is_audio_present("SPDIF_COAX_audio")):
                               
                                if (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD):
                                    SPDIF_test = True
                                    break                               
                                else:
                                    if (Audio_Counter == 2):
                                        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on SPDIF coaxial interface.")
                                        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_code  \
                                                                        + ";\n" + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_code  \
                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_message \
                                                                        + ";\n" + NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_message)
                                        NOS_API.set_error_message("SPDIF")
                                        error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_code
                                        error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.spdif_coaxial_signal_interference_error_message
                                        Audio_Counter = 3
        
                                    else:
                                        Audio_Counter = Audio_Counter + 1          
                            else:
                                if (Audio_Counter == 2):
                                    TEST_CREATION_API.write_log_to_file("Audio is not present on SPDIF coaxial interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message \
                                                                    + "; Audio is not present on SCART interface")
                                    NOS_API.set_error_message("SPDIF")
                                    error_codes = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.spdif_coaxial_signal_absence_error_message
                                    Audio_Counter = 3
                                else:
                                    Audio_Counter = Audio_Counter + 1
                                    
                        if(SPDIF_test):
                            TEST_CREATION_API.grabber_stop_audio_source()
                            time.sleep(1)
                            ## Start grabber device with video on default video source
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            
                            TEST_CREATION_API.send_ir_rc_command("[Factory_Reset]")
                            ## Perform grab picture
                            if not(NOS_API.grab_picture("Factory_Reset")):
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
                            
                            video_result = NOS_API.compare_pictures("Factory_Reset_ref", "Factory_Reset", "[Factory_Reset]")
                            
                            if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                                time.sleep(1)
                                TEST_CREATION_API.send_ir_rc_command("[Factory_Reset]")
                                ## Perform grab picture
                                if not(NOS_API.grab_picture("Factory_Reset_1")):
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
                                
                                video_result_1 = NOS_API.compare_pictures("Factory_Reset_ref", "Factory_Reset_1", "[Factory_Reset]")
                                
                                if not(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    TEST_CREATION_API.write_log_to_file("Navigation to resumo screen failed")
                                    NOS_API.set_error_message("Navegação")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message) 
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
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                                    time.sleep(2)
                            else:
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                time.sleep(2)
                                
                            if (NOS_API.wait_for_signal_present(35)):
                                if (NOS_API.wait_for_picture(["FTI_ref"], 30, "[FTI]", 0.0)):
                                    NOS_API.display_custom_dialog("Pressione no bot\xe3o 'Power'", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) 
                                    time.sleep(2)
                                    if (NOS_API.is_signal_present_on_video_source()):
                                        TEST_CREATION_API.write_log_to_file("Power button NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_button_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.power_button_nok_error_message)
                                        NOS_API.set_error_message("Botões")   
                                        error_codes = NOS_API.test_cases_results_info.power_button_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.power_button_nok_error_message  
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
                                    if (NOS_API.display_custom_dialog("O Led Vermelho est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                                        if (NOS_API.display_custom_dialog("O Display est\xe1 ligado?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):    
                                            ## Power off STB with energenie
                                            if (NOS_API.configure_power_switch_by_inspection()):
                                                if not(NOS_API.power_off()): 
                                                    TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                                                    
                                                    NOS_API.set_error_message("POWER SWITCH")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                                                    error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                                                    error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                                                    ## Return DUT to initial state and de-initialize grabber device
                                                    NOS_API.deinitialize()
                                                    NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                            
                                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                    report_file = NOS_API.create_test_case_log_file(
                                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                "",
                                                                end_time)
                                                    NOS_API.upload_file_report(report_file)
                                                    
                                                    NOS_API.send_report_over_mqtt_test_plan(
                                                            test_result,
                                                            end_time,
                                                            error_codes,
                                                            report_file)       
                                                    
                                                    ## Update test result
                                                    TEST_CREATION_API.update_test_result(test_result)
                                                    
                                                    return
                                            
                                            test_result = "PASS"
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Display NOK")
                                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.display_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.display_nok_error_message)
                                            NOS_API.set_error_message("Display")
                                            error_codes = NOS_API.test_cases_results_info.display_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.display_nok_error_message
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Led POWER Red NOK")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                                        NOS_API.set_error_message("Led's")
                                        error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message
                                else:
                                    TEST_CREATION_API.write_log_to_file("Factory Reset Fail")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                    NOS_API.set_error_message("Factory Reset") 
                                    error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                    error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message                            
                            else:
                                TEST_CREATION_API.write_log_to_file("Factory Reset Fail")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                                NOS_API.set_error_message("Factory Reset") 
                                error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                                error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message             
            #####################################################################################################################################      
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
  