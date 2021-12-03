import scipy.signal as ssig
import math
import numpy as np

class wav_homework:
  def __init__(self,file_1,file_2):
    self.file_1=file_1
    self.file_2=file_2
  
  def load_data(self):
    from scipy.io import wavfile
    n_fs, n_data= wavfile.read(self.file_1)
    p_fs, p_data= wavfile.read(self.file_2)
    return n_fs, n_data, p_fs , p_data
  
  def bandpass_filter(self, lowcut, highcut, data): 
    nyq= 0.5 * 44100
    b,a = ssig.butter(3,[lowcut/nyq,highcut/nyq],btype='band')
    w,h=ssig.freqz(b,a,44100)
    w_hz=w*44100/(2*math.pi)
    after_data=ssig.filtfilt(b,a,data)
    return w_hz,abs(h),after_data

  def filter_bank(self):
    w_hz_list,filter_bank_list=[],[]
    n_fs, n_data, p_fs , p_data=wav_homework.load_data(self)
    number=[200, 373, 629, 1006, 1561, 2381, 3590, 5372, 8000]; d_number=[n_data,p_data]
    for j in range (len(d_number)):
      after_sdata=0
      for i in range(0,len(number)-1):
        w_hz,fr_w,after_data=wav_homework.bandpass_filter(self,number[i],number[i+1],d_number[j]) # bandpassfilter
        w_hz_list = np.concatenate([w_hz_list, w_hz]) # filter bank x
        filter_bank_list=np.concatenate([filter_bank_list,fr_w]) # filter bank y
        after_sdata+=after_data
      if j==0: after_ndata=after_sdata
      if j==1: after_pdata=after_sdata
    return w_hz_list, filter_bank_list, after_ndata, after_pdata

  def make_envelope(self,data,fs):
    rms_data=[];data=data.tolist()
    for i in range(0,len(data)):
      slist=[x**2 for x in data[i:i+1000]]
      s2_list=math.sqrt(sum(slist)/len(slist))
      rms_data.extend([s2_list])
    return rms_data


  def show_result(self):
    n_fs, n_data, p_fs , p_data=wav_homework.load_data(self) # load sound data 
    w_hz,fr_h,after_ndata, after_pdata=wav_homework.filter_bank(self) # filter bank 
  #  ndata_envelope=wav_homework.make_envelope(self,after_ndata,n_fs)
  #  pdata_envelope=wav_homework.make_envelope(self,after_pdata,p_fs)
    n_envelope=wav_homework.make_envelope(self,after_ndata,n_fs)
    p_envelope=wav_homework.make_envelope(self,after_pdata,p_fs)
    import matplotlib.pyplot as plt 
    plt.figure(figsize=(10,8))
    plt.subplot(3,2,1);plt.specgram(n_data,Fs=n_fs);plt.title("Spectrogram 0_5n_cal");plt.xlabel("Time");plt.ylabel("Frequency")
    plt.subplot(3,2,2);plt.specgram(p_data,Fs=p_fs);plt.title("Spectrogram 0_5p_cal");plt.xlabel("Time");plt.ylabel("Frequency")
    plt.subplot(3,1,2);plt.plot(w_hz,fr_h,'black');plt.title("Filterbank");plt.xlabel("Time");plt.ylabel("Amplitude")
    plt.subplot(3,2,5);plt.plot(n_envelope,'black');plt.title("Envelope 0_5n_cal");plt.xlabel("Time");plt.ylabel("Frequency")
    plt.subplot(3,2,6);plt.plot(p_envelope,'black');plt.title("Envelope 0_5p_cal");plt.xlabel("Time");plt.ylabel("Frequency")    
    plt.tight_layout();plt.show()


if __name__=="__main__":
  wav_homework("0_5n_cal.wav","0_5p_cal.wav").show_result()

