cd 'C:\Users\rossvolkov\documents\python\sheets'

T = readtable('filtered_dataset.csv');

cd ../data

h = height(T);

for i = 1 : h
    patient_id = string(T{i, 1});
    audio = dir(strcat(patient_id, '\**\', string(T{i, 30}), '_audio.m4a')); 
    audio_location = strcat(audio.folder, '\', audio.name);
    output_dest = strcat(audio_location(1:strlength(audio_location)-9), 'spectral.wav');
%    countdown = dir(strcat(patient_id, '\**\', string(T{i, 31}), '_countdown.m4a'));
    
    
%     audiowrite('C:\Users\rossvolkov\desktop\y1.m4a', y1, Fs1);
%     [y2, Fs2] = audioread(strcat(countdown.folder, '\', countdown.name));
%     y3 = [y2; y1];

    
    try
        [y1, Fs1] = audioread(audio_location);
        output = v_specsub(y1, Fs1);    
        audiowrite(output_dest, output, Fs1);
    catch
        disp(i)
        continue
    end
end