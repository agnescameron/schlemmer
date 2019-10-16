j=0
for i in *.*;
  # echo "$j"
  do name=`echo "$i" | cut -d'.' -f1`
  echo "$name"
  ffmpeg -i "$i" -sample_fmt s16 -preset veryslow "${j}.wav"
  ((j++))
done




