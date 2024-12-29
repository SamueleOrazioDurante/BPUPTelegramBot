
import logger.logger as logger
import auth.tokenManager as tokenManager

import requests
import json
import traceback

TIKTOK_API_TOKEN = tokenManager.read_tiktok_token()
TWITTER_API_TOKEN = tokenManager.read_twitter_token()
INSTAGRAM_API_TOKEN = tokenManager.read_instagram_token()

def apiRequest(APIUrl,headers,query):

    logger.apiRequest(APIUrl,None)

    try:
        if query != None:
            response = requests.get(APIUrl, headers=headers, params=query)
        else:
            response = requests.get(APIUrl, headers=headers)

        logger.apiResponse(APIUrl,str(response.json()))
        return response.json()

    except Exception:
        logger.apiRequest(APIUrl,str(traceback.format_exc()))


TIKTOK_QUALITY = "hdplay" # default value (play,wmplay,hdplay)
# DA SPOSTARE IN .env

#DA SPOSTARE TUTTE RISPOSTE DI DEFUALT (USATE PER TESTING)

def TiktokAPIRequest(url):

    if not TIKTOK_API_TOKEN == None:
        APIUrl = "https://tiktok-download-without-watermark.p.rapidapi.com/analysis"

        headers = {
            "x-rapidapi-key": TIKTOK_API_TOKEN,
            "x-rapidapi-host": "tiktok-download-without-watermark.p.rapidapi.com"
        }

        querystring = {"url":url,"hd":"1"}

        jsonTik = apiRequest(APIUrl,headers,querystring)
        return jsonTik["data"][TIKTOK_QUALITY]

    else:
        return None
    
def TweetAPIRequest(url):
    
    if not TWITTER_API_TOKEN == None:
        APIUrl = "https://twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com/status"

        headers = {
            "x-rapidapi-key": TWITTER_API_TOKEN,
            "x-rapidapi-host": "twitter-downloader-download-twitter-videos-gifs-and-images.p.rapidapi.com"
        }

        querystring = {"url":url}


        jsonTweet = apiRequest(APIUrl,headers,querystring)

        # jsonTweet = {'created_at': 'Thu Mar 30 21:00:37 +0000 2023', 'id': 1641545992268025900, 'description': '✍️ @googledevgroups all across the globe are on the road to Google Cloud certification!\n\n#PrepWithGDG and level uup your career with Certification Study Groups, where participants can get hands on and attend instructor-led workshops → https://t.co/3cDiceXwkO https://t.co/EGwsJSx4v8', 'media': {'video': None, 'photo': [{'type': 'photo', 'url': 'https://pbs.twimg.com/media/FsfwUBoakAI25mp.jpg'}, {'type': 'photo', 'url': 'https://pbs.twimg.com/media/FsfwbZOakAoP7VC.jpg'}, {'type': 'photo', 'url': 'https://pbs.twimg.com/media/Fsfwf77akAs_ZLm.jpg'}]}, 'user': {'id': 50090898, 'id_str': '50090898', 'name': 'Google for Developers', 'screen_name': 'googledevs', 'description': 'Discover the latest developer tools, resources, events, and announcements to help you build smarter, ship faster. 🚀', 'followers_count': 2663488, 'friends_count': 309, 'listed_count': 17909, 'created_at': 'Tue Jun 23 20:25:29 +0000 2009', 'profile': 'https://pbs.twimg.com/profile_images/1804207283712200704/kBX_69dx_normal.png'}, 'retweet_count': 15, 'favorite_count': 74, 'lang': 'en'}

        # array object which contain 3 object (description,images_array,videos_array)

        images = []
        videos = []

        try:
            ### get images

            data = jsonTweet['media']['photo']

            if data != None:
                for item in data: 
                    images.append(item["url"])

            ### get videos

            data = jsonTweet['media']['video']

            if data != None:
            #    for item in data: 
            #        videos.append(item["videoVariants"][0]["url"])

                videos.append(jsonTweet['media']['video']['videoVariants'][1]['url'])
        except:
            pass

        post = [jsonTweet['description'],images,videos]

        return post
    
    else:
        return None

def InstaAPIRequest(reel_id):

    if not INSTAGRAM_API_TOKEN == None:
        url = "https://instagram-scraper-api2.p.rapidapi.com/v1/post_info/"
        url += reel_id

        headers = {
            "x-rapidapi-key": INSTAGRAM_API_TOKEN,
            "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
        }

        jsonReel = apiRequest(url,headers,None)

        #jsonReel = {"data":{"accessibility_caption":null,"are_remixes_crosspostable":true,"avatar_stickers":[],"boost_unavailable_identifier":null,"boost_unavailable_reason":null,"boost_unavailable_reason_v2":null,"can_reply":false,"can_reshare":true,"can_save":true,"caption":{"created_at":1735416521,"created_at_utc":1735416521,"did_report_as_spam":false,"hashtags":["#razer","#gamer","#gaming","#memes"],"id":3533250442263839403,"is_covered":false,"is_ranked_comment":false,"mentions":[],"pk":"18046723792951057","private_reply_status":0,"share_enabled":false,"text":"What’s your game of choice?\n\n#razer #gamer #gaming #memes","type":1},"caption_is_edited":true,"clips_metadata":{"achievements_info":{"num_earned_achievements":null,"show_achievements":false},"additional_audio_info":{"additional_audio_username":null,"audio_reattribution_info":{"should_allow_restore":false}},"asset_recommendation_info":null,"audio_canonical_id":"18477489445029529","audio_ranking_info":{"best_audio_cluster_id":"1121128503019641"},"audio_type":"original_sounds","branded_content_tag_info":{"can_add_tag":false},"breaking_content_info":null,"breaking_creator_info":null,"challenge_info":null,"clips_creation_entry_point":"clips","content_appreciation_info":{"enabled":false,"entry_point_container":null},"contextual_highlight_info":null,"cutout_sticker_info":[],"disable_use_in_clips_client_cache":false,"external_media_info":null,"featured_label":null,"is_fan_club_promo_video":false,"is_public_chat_welcome_video":false,"is_shared_to_fb":true,"mashup_info":{"can_toggle_mashups_allowed":false,"formatted_mashups_count":null,"has_been_mashed_up":false,"has_nonmimicable_additional_audio":false,"is_creator_requesting_mashup":false,"is_light_weight_check":true,"is_light_weight_reuse_allowed_check":false,"is_pivot_page_available":false,"is_reuse_allowed":true,"mashup_type":null,"mashups_allowed":true,"non_privacy_filtered_mashups_media_count":0,"original_media":null,"privacy_filtered_mashups_media_count":null},"merchandising_pill_info":null,"music_info":null,"nux_info":null,"original_sound_info":{"allow_creator_to_rename":true,"attributed_custom_audio_asset_id":null,"audio_asset_id":1877584959314069,"audio_asset_start_time_in_ms":null,"audio_filter_infos":[],"audio_parts":[],"audio_parts_by_filter":[],"can_remix_be_shared_to_fb":true,"can_remix_be_shared_to_fb_expansion":false,"consumption_info":{"display_media_id":null,"is_bookmarked":false,"is_trending_in_clips":false,"should_mute_audio_reason":"","should_mute_audio_reason_type":null},"duration_in_ms":33066,"fb_downstream_use_xpost_metadata":null,"formatted_clips_media_count":null,"hide_remixing":false,"ig_artist":{"full_name":"RΛZΞR","id":"270603774","is_private":false,"is_verified":true,"pk":270603774,"profile_pic_id":"3307113797516129594_270603774","profile_pic_url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-19/428911771_7321246877932284_2697368309249970907_n.jpg?stp=dst-jpg_e0_s150x150_tt6&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=8xIl4XeXAuMQ7kNvgHpzA6H&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYDek5LWIjawsiPXWvdzxhVE8Bz_x58S6VxuIWHrTFw96Q&oe=677746BB&_nc_sid=fc8dfb","username":"razer"},"is_audio_automatically_attributed":false,"is_eligible_for_audio_effects":true,"is_eligible_for_vinyl_sticker":true,"is_explicit":false,"is_original_audio_download_eligible":true,"is_reuse_disabled":false,"is_xpost_from_fb":false,"oa_owner_is_music_artist":false,"original_audio_subtype":"default","original_audio_title":"Original audio","original_media_id":3533250442263839403,"overlap_duration_in_ms":null,"previous_trend_rank":null,"progressive_download_url":"https://scontent-vie1-1.xx.fbcdn.net/o1/v/t2/f2/m69/AQMMmtnMrz0Vxa_Syr5-ynJx8tgkx5aa-bkozs2v8kRn55hxm6XLMOGTHaTuMYvkuCJXzM_M3ifwn1Ff2wbFFgj1.mp4?strext=1&_nc_cat=109&_nc_sid=8bf8fe&_nc_ht=scontent-vie1-1.xx.fbcdn.net&_nc_ohc=nalcxyrBRI4Q7kNvgEhAo0-&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5BVURJT19PTkxZLi5DMy4wLnByb2dyZXNzaXZlX2F1ZGlvIiwieHB2X2Fzc2V0X2lkIjoyOTc0MDA1ODQyNzM4ODgzLCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=9-4&_nc_zt=28&oh=00_AYB74etqY2s9lkY-0RdZqNvkk9kg5gpgLumBt0dt2xLCDw&oe=67774EA0","should_mute_audio":false,"time_created":1735416398,"trend_rank":null,"xpost_fb_creator_info":null},"originality_info":null,"professional_clips_upsell_type":0,"reels_on_the_rise_info":null,"reusable_text_attribute_string":null,"reusable_text_info":null,"shopping_info":null,"show_achievements":false,"show_tips":null,"template_info":null,"viewer_interaction_settings":null},"clips_tab_pinned_user_ids":[],"coauthor_producer_can_see_organic_insights":false,"coauthor_producers":[],"code":"DEIoI6poMKr","comment_inform_treatment":{"action_type":null,"should_have_inform_treatment":false,"text":"","url":null},"comment_threading_enabled":true,"comments_disabled":null,"commerce_integrity_review_decision":"","commerciality_status":"not_commercial","creator_viewer_insights":[],"crosspost_metadata":{},"deleted_reason":0,"device_timestamp":1735416282710716,"fb_aggregated_comment_count":0,"fb_aggregated_like_count":0,"fb_user_tags":{"in":[]},"fbid":"18046723252951057","featured_products":[],"filter_type":0,"fundraiser_tag":{"has_standalone_fundraiser":false},"gen_ai_detection_method":{"detection_method":"NONE"},"has_audio":true,"has_high_risk_gen_ai_inform_treatment":false,"has_liked":false,"has_more_comments":true,"has_privately_liked":false,"has_shared_to_fb":0,"has_views_fetching":true,"id":"3533250442263839403_270603774","ig_media_sharing_disabled":false,"ig_play_count":212388,"igbio_product":null,"image_versions":{"additional_items":{"first_frame":{"height":852,"url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-15/470919276_1266880524631062_3289354931610288116_n.jpg?stp=dst-jpg_e15_p480x480_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi42NDB4MTEzNi5zZHIuZjcxODc4LmFkZGl0aW9uYWxfY292ZXJfZnJhbWUifQ&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=106&_nc_ohc=JfPTH9AeV8sQ7kNvgG_VCJs&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYA3e4xdyp_p5VbndnVe1JhLCN2QDimFAn6pzfJeAi37UA&oe=677753D4&_nc_sid=fc8dfb","width":480},"igtv_first_frame":{"height":852,"url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-15/470919276_1266880524631062_3289354931610288116_n.jpg?stp=dst-jpg_e15_p480x480_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi42NDB4MTEzNi5zZHIuZjcxODc4LmFkZGl0aW9uYWxfY292ZXJfZnJhbWUifQ&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=106&_nc_ohc=JfPTH9AeV8sQ7kNvgG_VCJs&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYA3e4xdyp_p5VbndnVe1JhLCN2QDimFAn6pzfJeAi37UA&oe=677753D4&_nc_sid=fc8dfb","width":480},"smart_frame":null},"items":[{"height":854,"url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-15/471646288_18477135322011775_3795470853896255871_n.jpg?stp=dst-jpg_e15_p480x480_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMjkweDIyOTQuc2RyLmY3NTc2MS5kZWZhdWx0X2NvdmVyX2ZyYW1lIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=107&_nc_ohc=nO45idmb_aMQ7kNvgEL7FGn&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=MzUzMzI1MDQ0MjI2MzgzOTQwMw%3D%3D.3-ccb7-5&oh=00_AYDFfXR4eAWPBNkY9WvfUSqBr6mVFaoItjjXUeQ7_ecFsg&oe=67774B2D&_nc_sid=fc8dfb","width":480}],"scrubber_spritesheet_info_candidates":{"default":{"file_size_kb":435,"max_thumbnails_per_sprite":105,"rendered_width":96,"sprite_height":1246,"sprite_urls":["https://scontent-vie1-1.cdninstagram.com/v/t51.2885-15/471975321_8895132027228943_1633693917359031175_n.jpg?_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=107&_nc_ohc=dQAHoyGdIusQ7kNvgHgwC4V&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYAmhunl7WxE3Zq1HpEjgr2tfeHvv4ihoBsD7-07-VhGfw&oe=67776DF0&_nc_sid=fc8dfb"],"sprite_width":1500,"thumbnail_duration":0.31491428571428576,"thumbnail_height":178,"thumbnail_width":100,"thumbnails_per_row":15,"total_thumbnail_num_per_sprite":105,"video_length":33.066}}},"inline_composer_display_condition":"impression_trigger","inline_composer_imp_trigger_time":5,"integrity_review_decision":"pending","invited_coauthor_producers":[],"is_artist_pick":false,"is_comments_gif_composer_enabled":true,"is_cutout_sticker_allowed":false,"is_dash_eligible":1,"is_eligible_for_media_note_recs_nux":false,"is_eligible_for_meta_ai_share":false,"is_in_profile_grid":false,"is_open_to_public_submission":false,"is_organic_product_tagging_eligible":false,"is_paid_partnership":false,"is_pinned":false,"is_post_live_clips_media":false,"is_quiet_post":false,"is_reshare_of_text_post_app_media_in_ig":false,"is_reuse_allowed":true,"is_social_ufi_disabled":false,"is_tagged_media_shared_to_viewer_profile_grid":false,"is_third_party_downloads_eligible":true,"is_unified_video":false,"is_video":true,"like_and_view_counts_disabled":false,"location":null,"max_num_visible_preview_comments":2,"media_cropping_info":{"square_crop":{"crop_bottom":0.0,"crop_left":0.0,"crop_right":0.0,"crop_top":0.0}},"media_name":"reel","media_notes":{"items":[]},"media_type":2,"meta_ai_suggested_prompts":[],"metrics":{"comment_count":130,"fb_like_count":0,"fb_play_count":22,"like_count":12594,"play_count":212410,"save_count":null,"share_count":4852,"user_follower_count":null,"user_media_count":null,"view_count":null},"music_metadata":null,"number_of_qualities":6,"open_carousel_show_follow_button":false,"original_height":1920,"original_width":1080,"owner":{"account_badges":[],"account_type":2,"can_see_quiet_post_attribution":true,"fan_club_info":{"autosave_to_exclusive_highlight":null,"connected_member_count":null,"fan_club_id":null,"fan_club_name":null,"fan_consideration_page_revamp_eligiblity":null,"has_created_ssc":null,"has_enough_subscribers_for_ssc":null,"is_fan_club_gifting_eligible":null,"is_fan_club_referral_eligible":null,"is_free_trial_eligible":null,"largest_public_bc_id":null,"subscriber_count":null},"fbid_v2":17841400353224228,"feed_post_reshare_disabled":false,"full_name":"RΛZΞR","has_anonymous_profile_picture":false,"id":"270603774","is_active_on_text_post_app":true,"is_favorite":false,"is_private":false,"is_unpublished":false,"is_verified":true,"latest_reel_media":0,"pk":270603774,"profile_pic_id":"3307113797516129594_270603774","profile_pic_url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-19/428911771_7321246877932284_2697368309249970907_n.jpg?stp=dst-jpg_e0_s150x150_tt6&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=8xIl4XeXAuMQ7kNvgHpzA6H&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYDek5LWIjawsiPXWvdzxhVE8Bz_x58S6VxuIWHrTFw96Q&oe=677746BB&_nc_sid=fc8dfb","show_account_transparency_details":true,"text_post_app_is_private":false,"third_party_downloads_enabled":1,"transparency_product_enabled":false,"username":"razer"},"pk":3533250442263839403,"preview_comments":[],"product_suggestions":[],"product_type":"clips","share_count_disabled":false,"sharing_friction_info":{"bloks_app_url":null,"sharing_friction_payload":null,"should_have_sharing_friction":false},"shop_routing_user_id":null,"should_show_author_pog_for_tagged_media_shared_to_profile_grid":false,"subscribe_cta_visible":false,"tagged_users":null,"taken_at":1735416394,"thumbnail_url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-15/471646288_18477135322011775_3795470853896255871_n.jpg?stp=dst-jpg_e15_p480x480_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMjkweDIyOTQuc2RyLmY3NTc2MS5kZWZhdWx0X2NvdmVyX2ZyYW1lIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=107&_nc_ohc=nO45idmb_aMQ7kNvgEL7FGn&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=MzUzMzI1MDQ0MjI2MzgzOTQwMw%3D%3D.3-ccb7-5&oh=00_AYDFfXR4eAWPBNkY9WvfUSqBr6mVFaoItjjXUeQ7_ecFsg&oe=67774B2D&_nc_sid=fc8dfb","timeline_pinned_user_ids":[],"top_likers":[],"user":{"account_badges":[],"account_type":2,"can_see_quiet_post_attribution":true,"fan_club_info":{"autosave_to_exclusive_highlight":null,"connected_member_count":null,"fan_club_id":null,"fan_club_name":null,"fan_consideration_page_revamp_eligiblity":null,"has_created_ssc":null,"has_enough_subscribers_for_ssc":null,"is_fan_club_gifting_eligible":null,"is_fan_club_referral_eligible":null,"is_free_trial_eligible":null,"largest_public_bc_id":null,"subscriber_count":null},"fbid_v2":17841400353224228,"feed_post_reshare_disabled":false,"full_name":"RΛZΞR","has_anonymous_profile_picture":false,"id":"270603774","is_active_on_text_post_app":true,"is_favorite":false,"is_private":false,"is_unpublished":false,"is_verified":true,"latest_reel_media":0,"profile_pic_id":"3307113797516129594_270603774","profile_pic_url":"https://scontent-vie1-1.cdninstagram.com/v/t51.2885-19/428911771_7321246877932284_2697368309249970907_n.jpg?stp=dst-jpg_e0_s150x150_tt6&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=1&_nc_ohc=8xIl4XeXAuMQ7kNvgHpzA6H&_nc_gid=7a6291bd59fc4229b8aa26c306e10c41&edm=ALQROFkBAAAA&ccb=7-5&oh=00_AYDek5LWIjawsiPXWvdzxhVE8Bz_x58S6VxuIWHrTFw96Q&oe=677746BB&_nc_sid=fc8dfb","show_account_transparency_details":true,"text_post_app_is_private":false,"third_party_downloads_enabled":1,"transparency_product_enabled":false,"username":"razer"},"video_codec":"vp09.00.31.08.00.01.01.01.00","video_duration":33.066,"video_sticker_locales":[],"video_subtitles_confidence":0.6899999976158142,"video_subtitles_locale":"en_US","video_url":"https://scontent-vie1-1.cdninstagram.com/o1/v/t16/f2/m86/AQOhGDI-1beXW9Sek4lJMa5HNuLawJJOv4TYn8T5YW3ZE3z-SBryoyDVDZgk-lUbo8xaxGPcD4Xb_1LzYALTgPd0N80dTB7NKlBJdp8.mp4?efg=eyJ4cHZfYXNzZXRfaWQiOjI5NzQwMDU4NDI3Mzg4ODMsInZlbmNvZGVfdGFnIjoieHB2X3Byb2dyZXNzaXZlLklOU1RBR1JBTS5DTElQUy5DMy43MjAuZGFzaF9iYXNlbGluZV8xX3YxIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=100&vs=42ac82a79d04b1d5&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC84QzQxOTlCNzhEMUQ0RUQ3MzExNEUxM0FDMDg5NjNCMF92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dPcE5HUnhMNEhmWDBpa0NBSlMtNVYzLTYxTTZicV9FQUFBRhUCAsgBACgAGAAbAogHdXNlX29pbAExEnByb2dyZXNzaXZlX3JlY2lwZQExFQAAJob7h532tcgKFQIoAkMzLBdAQIhysCDEnBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1_gcA&ccb=9-4&oh=00_AYCknzaH7kFKvird219_LPdMEbhG39wAOaFRA9S8e2cGew&oe=67734589&_nc_sid=1d576d","video_versions":[{"bandwidth":770504,"height":1280,"id":"2181670232227227v","type":101,"url":"https://scontent-vie1-1.cdninstagram.com/o1/v/t16/f2/m86/AQOhGDI-1beXW9Sek4lJMa5HNuLawJJOv4TYn8T5YW3ZE3z-SBryoyDVDZgk-lUbo8xaxGPcD4Xb_1LzYALTgPd0N80dTB7NKlBJdp8.mp4?efg=eyJ4cHZfYXNzZXRfaWQiOjI5NzQwMDU4NDI3Mzg4ODMsInZlbmNvZGVfdGFnIjoieHB2X3Byb2dyZXNzaXZlLklOU1RBR1JBTS5DTElQUy5DMy43MjAuZGFzaF9iYXNlbGluZV8xX3YxIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=100&vs=42ac82a79d04b1d5&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC84QzQxOTlCNzhEMUQ0RUQ3MzExNEUxM0FDMDg5NjNCMF92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dPcE5HUnhMNEhmWDBpa0NBSlMtNVYzLTYxTTZicV9FQUFBRhUCAsgBACgAGAAbAogHdXNlX29pbAExEnByb2dyZXNzaXZlX3JlY2lwZQExFQAAJob7h532tcgKFQIoAkMzLBdAQIhysCDEnBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1_gcA&ccb=9-4&oh=00_AYCknzaH7kFKvird219_LPdMEbhG39wAOaFRA9S8e2cGew&oe=67734589&_nc_sid=1d576d","width":720},{"bandwidth":770504,"height":640,"id":"929728015799446v","type":102,"url":"https://scontent-vie1-1.cdninstagram.com/o1/v/t16/f2/m86/AQP3_haBeM4x0DVQdoWZCGtBWu9_zZ5Cw3POr8JokLaUxSyIMbpFCM1Uy-tTbK3MHnPmK5jUl-D_cyXnfolxYIjxABmG-T_KSKD1Kj0.mp4?efg=eyJ4cHZfYXNzZXRfaWQiOjI5NzQwMDU4NDI3Mzg4ODMsInZlbmNvZGVfdGFnIjoieHB2X3Byb2dyZXNzaXZlLklOU1RBR1JBTS5DTElQUy5DMy4zNjAuZGFzaF9iYXNlbGluZV8zX3YxIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=102&vs=e2aa235c2e803e98&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC9BOTRDQUUyMjQyQzZENjlCNTU0RDIxM0FBMEYyM0M4OF92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dPcE5HUnhMNEhmWDBpa0NBSlMtNVYzLTYxTTZicV9FQUFBRhUCAsgBACgAGAAbAogHdXNlX29pbAExEnByb2dyZXNzaXZlX3JlY2lwZQExFQAAJob7h532tcgKFQIoAkMzLBdAQIhysCDEnBgSZGFzaF9iYXNlbGluZV8zX3YxEQB1_gcA&ccb=9-4&oh=00_AYDfFlTcdRsxPFXduxleLmemGXvJ8fZLER6Ahzd1pYaZKw&oe=677360F3&_nc_sid=1d576d","width":360},{"bandwidth":770504,"height":640,"id":"929728015799446v","type":103,"url":"https://scontent-vie1-1.cdninstagram.com/o1/v/t16/f2/m86/AQP3_haBeM4x0DVQdoWZCGtBWu9_zZ5Cw3POr8JokLaUxSyIMbpFCM1Uy-tTbK3MHnPmK5jUl-D_cyXnfolxYIjxABmG-T_KSKD1Kj0.mp4?efg=eyJ4cHZfYXNzZXRfaWQiOjI5NzQwMDU4NDI3Mzg4ODMsInZlbmNvZGVfdGFnIjoieHB2X3Byb2dyZXNzaXZlLklOU1RBR1JBTS5DTElQUy5DMy4zNjAuZGFzaF9iYXNlbGluZV8zX3YxIn0&_nc_ht=scontent-vie1-1.cdninstagram.com&_nc_cat=102&vs=e2aa235c2e803e98&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC9BOTRDQUUyMjQyQzZENjlCNTU0RDIxM0FBMEYyM0M4OF92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dPcE5HUnhMNEhmWDBpa0NBSlMtNVYzLTYxTTZicV9FQUFBRhUCAsgBACgAGAAbAogHdXNlX29pbAExEnByb2dyZXNzaXZlX3JlY2lwZQExFQAAJob7h532tcgKFQIoAkMzLBdAQIhysCDEnBgSZGFzaF9iYXNlbGluZV8zX3YxEQB1_gcA&ccb=9-4&oh=00_AYDfFlTcdRsxPFXduxleLmemGXvJ8fZLER6Ahzd1pYaZKw&oe=677360F3&_nc_sid=1d576d","width":360}]}}
        

    # json object contain a main media

        images = []
        videos = []

        try:

            ### get main media

            # video first
            try:

                video = jsonReel['data']['video_url'] 
                videos.append(video)

            except:
                # then image
                try:

                    image = jsonReel['data']['image_versions']['item'][0]['url']
                    images.append(video)

                except:
                    pass

        except:
            pass

        post = [jsonReel['data']['caption']['text'],images,videos]

        return post
    
    else:
        return None