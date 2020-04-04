# dance-pose

## prepare
### download video from iqiyi

```
pip install you-get
you-get https://www.iqiyi.com/v_19rx3k0t0g.html?list=19rqwueh0q
```

### make videos to pictures



### run alphapose

```
python demo.py --indir videos/1 --outdir output/1 --format cmu
```

### make pictures to video

ffmpeg -y -f image2 -r 30 -i output/1/%5d.png -vcodec libx264 -b 2000k 1.mp4


