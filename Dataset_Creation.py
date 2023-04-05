
@AUTHOR #ITS_CANDELS
#05/04/2023
#import the necessary packages


import imutils
import time
import cv2
from datetime import datetime as dt
# import pandas as pd
from moviepy.editor import VideoFileClip
from pathlib import Path
import os 
start=time.time()


#INITIALIZE BACKGROUND SUBTRACTOR

fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()


#INIZIALIZE TIME

start_time = time.time()    
now=dt.now()
now_time= now.strftime("%m_%d_%Y_%H:%M:%S")
print("DATA E ORA:",now_time)
elapsed=time.time()-start




#PATH
db= ("INPUT_VIDEO")


#LIST
lista_array=[]
h=[]
m=[]
s=[]
ms=[]
lista_csv=[]
lista_array.insert(0,0)


#COUNTER
count = 0
cc=0
frames=0





captured = False

#RENAME_ALL_FILES
files = os.listdir(db)

counter2=0
for index, file in enumerate(files):
    counter2+=1
    dir=os.rename(os.path.join(db, file), os.path.join(db, 'video' .join([str(counter2), '.mp4'])))


pathvideo= Path(db).glob('**/*.mp4')
data_dir_list = list(pathvideo)


for i in data_dir_list:
    cc+=1
    change_frame = 0
    candels=0
    frames=0


    

    d=str(i)
    

    path=os.path.dirname(d)
    

    print('NEW___VIDEO___NAME___ = '+str(path)+'/'+'video '+'('+str(cc)+')'+'.mp4')

    
    
    
    

    cap = cv2.VideoCapture(d)
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('FPS NUMBER: '+str(fps))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('FRAMES NUMBER: '+str(frame_count))
    (W, H) = (None, None)
    
    
        

    while True:


        (grabbed, frame) = cap.read()
    

        change_frame +=1
        
        if frame is None:
            break
    	

        orig = frame.copy()
        frame = imutils.resize(frame, width=600)
        mask = fgbg.apply(frame)
        

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
       
        if W is None or H is None:
            (H, W) = mask.shape[:2]
            
            
            
    	
        #TIMESTAMP
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
    
        seconds = int(milliseconds//1000)
        milliseconds =milliseconds%1000
        minutes = 0
        hours = 0
        
        if hours >= 60:
            minutes = int(hours//60)
            hours = int(hours % 60)
    
        if seconds >= 60:
    
            minutes =int(seconds//60)
            seconds = int(seconds % 60)
    
        if minutes >= 60:
            hours = int(minutes//60)
            minutes = int(minutes % 60)
            
        ore=(f'{hours:02}')
        minuti=(f'{minutes:02}')
        secondi=(f'{seconds:02}')
            
        timestamp=(f'{hours:02}'+':'+f'{minutes:02}'+':'+f'{seconds:02}')
        
        
        
        
        
        #Compute the percentage of the mask that is "foreground"
        p = (cv2.countNonZero(mask) / float(W * H)) * 100
    

    
        if p < 0.50 and not captured and frames > int(fps*2):
            lista_array.append(change_frame)
            u=[x - abs(lista_array[i-1]) if i else None for i, x in enumerate(lista_array)][1:]           
            diff=u[candels]

            
            durata=abs(diff/fps)
            
            start=change_frame/fps
            endtime=start+durata

            count+=1
                        
            outputfile='OUTPUT_FILE_MINIVIDEO/VIDEO_N_'+str(cc)+'_SCENA_'+str(count)+'.mp4'
            
            required_video_file=VideoFileClip('INPUT_VIDEO/'+str(cc)+'video.'+'mp4')            
           
            full_duration=required_video_file.duration
            
            
            
            
            
            if start > full_duration:
                print(f"video too short to get {start}-{endtime} (full duration: {full_duration})")
                break  
            
            if endtime > full_duration:
                print(f"crop endtime {endtime} to {full_duration}")
                endtime = full_duration
            
            
            
            clip =  required_video_file.subclip (start, endtime)
            clip.to_videofile (outputfile, codec="libx264", temp_audiofile='temp-audio'+str(cc)+'.m4a', remove_temp=True, audio_codec='aac')

            candels+=1
            

            print('')
            print('TOTAL_VIDEO_DURATION '+str(full_duration))
            print('')
            print('VIDEO_NAME '+('VIDEO_ELABORATION/'+'video '+'('+str(cc)+')'+'.mp4'))
            print('')
            print('START: ' +str(start))
            print('SCENA N°'+ str(count))
            print('H:M:S '+timestamp) 
            
            print('END: ' +str(endtime))
            print('')
            print('DURATION_MINIVIDEO: '+str(durata))
            print('')
    
            captured = True       

    	
            lista_csv.append(timestamp)

        elif captured and p >=15:
              
            captured = False
            

        key = cv2.waitKey(1) & 0xFF
    	
        #if the `x` key was pressed, break from the loop
        if key == ord("x"):
            break
    	

        frames += 1

    

    
    
    
    cap.release()
    #DECOMMENT IF YOU WANT REPORT 
   
    # lista = pd.DataFrame(lista_csv)
    # lista.to_csv(r'OUTPUT_PAZIENTI_NORMALI/Totalvideo.csv', header=False, index=False)    
    
    
    #END ELABORATION TIME
    elapsed=time.time()-start
    output=dt.strftime(dt.utcfromtimestamp(elapsed), '%H:%M:%S')
    print("TEMPOELABORAZIONE:",output)
