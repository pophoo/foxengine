# -*- coding: utf-8 -*-

'''
    用于计算一些关键值

'''

from wolfox.fengine.ifuture.ibase import *


'''
    计算顶点及其级别
    不看右边。即如果不停创新高，则顶点不停在移动
    以小级别的顶/底来确认高级别的低/顶
'''
peaks_len = (5,15,30,60,120,270,540,810)
def peak(sif):

    hpeaks,lpeaks = [],[]   #顶点顺序集合
    hline,lline,line = [],[],[] #折返集合
    lmax,lmin = [],[]
    for il in peaks_len:
        hpeaks.append([])
        lpeaks.append([])
        hline.append([])
        lline.append([])
        line.append([])
        lmax.append(tmax(sif.close,il))
        lmin.append(tmin(sif.close,il))

    #print line
    slen = len(sif.close)
    ch,cl = 0,99999999
    for ci,chigh,clow in zip(range(slen),sif.high,sif.low):
        if chigh > ch:  #顶点
            hpeak(sif,chigh,ci,hpeaks,lpeaks,lmax,peaks_len,hline,lline,line)
        if clow < cl:  #底点
            lpeak(sif,clow,ci,hpeaks,lpeaks,lmin,peaks_len,hline,lline,line)
        ch = chigh
        cl = clow
    sif.peaks_len = peaks_len
    sif.hpeaks = hpeaks
    sif.lpeaks = lpeaks
    sif.hline = hline
    sif.lline = lline
    sif.line = line


'''
    计算高点
'''
def hpeak(sif,chigh,ci,hpeaks,lpeaks,lmax,peaks_len,hline,lline,line):
    dS = sif.close - rollx(sif.close) #当分钟内的实际行程
    tW = np.abs(dS * sif.vol)
    for pl,hpk,lpk,ll,ihl,ill,il in zip(peaks_len,hpeaks,lpeaks,lmax,hline,lline,line):
        if hpk == [] or chigh > hpk[-1][0] or (ci-hpk[-1][1] >= pl and chigh >= ll[ci]):    #不用not hpk，不清晰
            #hpk为空，或 出现新高点，或超过时间界限，并且是最近len周期的高点
            #if hpk != []: print sif.date[ci],sif.time[ci],chigh,hpk[-1][0],ci
            hpk.append((chigh,ci))   #高点及其坐标
            if lpk != []:
                ln = BaseObject(start=lpk[-1],end=hpk[-1],tlength=hpk[-1][1]-lpk[-1][1],slength=hpk[-1][0]-lpk[-1][0],svol=np.sum(sif.vol[lpk[-1][1]:hpk[-1][1]+1]),holding=sif.holding[ci])
                ln.v = ln.slength * 1.0 / ln.tlength
                ln.e = ln.holding * ln.v * ln.v / 2    #能量
                ln.w = np.sum(tW[lpk[-1][1]:hpk[-1][1]]+1)
                ln.p = ln.w / ln.tlength
                ihl.append(ln)
                il.append(ln)
        else:   #不比前一小级别高点高，则退出下一级别的比较
            break


'''
    计算低点
'''
def lpeak(sif,clow,ci,hpeaks,lpeaks,lmin,peaks_len,hline,lline,line):
    dS = sif.close - rollx(sif.close) #当分钟内的实际行程
    tW = np.abs(dS * sif.vol)
    for pl,hpk,lpk,ll,ihl,ill,il in zip(peaks_len,hpeaks,lpeaks,lmin,hline,lline,line):
        if lpk == [] or clow < lpk[-1][0] or (ci-lpk[-1][1] >= pl and clow <= ll[ci]):    #不用not lpk，不清晰
            #lpk为空，或 出现新高点，或超过时间界限，并且是最近len周期的低点
            #if lpk != []: print sif.date[ci],sif.time[ci],clow,lpk[-1][0],ci
            lpk.append((clow,ci))   #低点及其坐标
            if hpk != []:
                ln = BaseObject(start=hpk[-1],end=lpk[-1],tlength=lpk[-1][1]-hpk[-1][1],slength=lpk[-1][0]-hpk[-1][0],svol=np.sum(sif.vol[hpk[-1][1]:lpk[-1][1]+1]),holding=sif.holding[ci])
                ln.v = ln.slength * 1.0 / ln.tlength
                ln.e = ln.holding * ln.v * ln.v / 2    #能量
                ln.w = -np.sum(tW[hpk[-1][1]:lpk[-1][1]]+1)
                ln.p = ln.w / ln.tlength
                ill.append(ln)
                il.append(ln)
        else:   #不比前一小级别低点低，则退出下一级别的比较
            break



def peakline_save(sif,line,fname):
    '''
        fcore.peakline_save(i00,i00.line[0],'d:/temp/peak5_line.txt')
        fcore.peakline_save(i00,i00.line[1],'d:/temp/peak15_line.txt')
        fcore.peakline_save(i00,i00.line[2],'d:/temp/peak30_line.txt')
        fcore.peakline_save(i00,i00.line[3],'d:/temp/peak60_line.txt')
        fcore.peakline_save(i00,i00.line[4],'d:/temp/peak120_line.txt')
        fcore.peakline_save(i00,i00.line[5],'d:/temp/peak270_line.txt')
        fcore.peakline_save(i00,i00.line[6],'d:/temp/peak540_line.txt')
        fcore.peakline_save(i00,i00.line[7],'d:/temp/peak810_line.txt')
    '''
    fh = open(fname,'w+')
    pre = None
    for il in line:
        #print >>fh,il.start,il.end,sif.date[il.start[1]],sif.time[il.start[1]],sif.date[il.end[1]],sif.time[il.end[1]],il.tlength,il.slength,il.slength*1.0/il.tlength,il.slength*il.tlength,il.slength*il.tlength*1.0/il.svol
        dFE = dFV = 0
        if pre:
            de = svol = 0
            if (il.v > 0 and pre.v>0):
                de = (il.e - pre.e)*1.0
                svol = il.svol - pre.svol                
            elif (il.v<0 and pre.v<0):
                de = (il.e - pre.e)*(-1.0)
                svol = il.svol - pre.svol                
            elif (il.v>0 and pre.v<0):
                de = (il.e + pre.e)*1.0
                svol = il.svol
            elif (il.v<0 and pre.v>0):
                de = (il.e + pre.e)*(-1.0)
                svol = il.svol
            dFE = de / abs(il.slength)
            #fu = (de /abs(il.slength) + svol)/2
            #fd = (-de /abs(il.slength) + svol)/2
        else:
            sF = fu = fd = 0
        if pre:
            slen = svol = v0 = t = 0
            if (il.v > 0 and pre.v>0):
                svol = il.svol - pre.svol
                slen = il.slength-pre.slength
                v0 = pre.v
                t = il.tlength - pre.tlength
            elif (il.v<0 and pre.v<0):
                svol = il.svol - pre.svol
                slen = il.slength-pre.slength                
                vo = pre.v
                t = il.tlength - pre.tlength                
            else:
                svol = il.svol
                slen = il.slength
                v0 = 0
                t = il.tlength
            dFV = 2 * (pre.holding + il.holding)/2 * (slen - v0*t) /t/t
            #sF = svol
            #fu = (dF + sF)/2
            #fd = (sF - dF)/2
        else:
            sF = fu = fd = 0

        mk = dFV/dFE if dFE!=0 else 0

        print >>fh,il.start[0],il.end[0],sif.date[il.start[1]],sif.time[il.start[1]],sif.date[il.end[1]],sif.time[il.end[1]],il.tlength,il.slength,il.slength*il.tlength,il.v,il.e,il.w,il.p
        #print >>fh,il.start[0],il.end[0],sif.date[il.start[1]],sif.time[il.start[1]],sif.time[il.end[1]],round(de),round(il.svol)
        pre = il
    fh.close()

'''
fcore.peakline_save(i00,i00.line[0],'d:/temp/peak5_line.txt')
fcore.peakline_save(i00,i00.line[1],'d:/temp/peak15_line.txt')
fcore.peakline_save(i00,i00.line[2],'d:/temp/peak30_line.txt')
fcore.peakline_save(i00,i00.line[3],'d:/temp/peak60_line.txt')
fcore.peakline_save(i00,i00.line[4],'d:/temp/peak120_line.txt')
fcore.peakline_save(i00,i00.line[5],'d:/temp/peak270_line.txt')
fcore.peakline_save(i00,i00.line[6],'d:/temp/peak540_line.txt')
fcore.peakline_save(i00,i00.line[7],'d:/temp/peak810_line.txt')

fcore.peakline_save(i00,i00.hline[0],'d:/temp/peak5_hline.txt')
fcore.peakline_save(i00,i00.hline[1],'d:/temp/peak15_hline.txt')
fcore.peakline_save(i00,i00.hline[2],'d:/temp/peak30_hline.txt')
fcore.peakline_save(i00,i00.hline[3],'d:/temp/peak60_hline.txt')
fcore.peakline_save(i00,i00.hline[4],'d:/temp/peak120_hline.txt')
fcore.peakline_save(i00,i00.hline[5],'d:/temp/peak270_hline.txt')
fcore.peakline_save(i00,i00.hline[6],'d:/temp/peak540_hline.txt')
fcore.peakline_save(i00,i00.hline[7],'d:/temp/peak810_hline.txt')

fcore.peakline_save(i00,i00.lline[0],'d:/temp/peak5_lline.txt')
fcore.peakline_save(i00,i00.lline[1],'d:/temp/peak15_lline.txt')
fcore.peakline_save(i00,i00.lline[2],'d:/temp/peak30_lline.txt')
fcore.peakline_save(i00,i00.lline[3],'d:/temp/peak60_lline.txt')
fcore.peakline_save(i00,i00.lline[4],'d:/temp/peak120_lline.txt')
fcore.peakline_save(i00,i00.lline[5],'d:/temp/peak270_lline.txt')
fcore.peakline_save(i00,i00.lline[6],'d:/temp/peak540_lline.txt')
fcore.peakline_save(i00,i00.lline[7],'d:/temp/peak810_lline.txt')

'''


'''
    计算日内极点
    第一点必然即是最高也是最低
'''
def dpeak(sif):
    pred = 0
    sh = np.zeros_like(sif.close)
    sl = np.zeros_like(sif.close)

    shl = np.zeros_like(sif.close)  #高点时的低
    slh = np.zeros_like(sif.close)  #低点时的高

    ih = np.zeros_like(sif.close)
    il = np.zeros_like(sif.close)
    curh,curl = 0,99999999
    icurh,icurl = 0,0
    curhl,curlh = 0,0
    for ii,dt,tt,h,l,c in zip(range(len(sif.close)),sif.date,sif.time,sif.high,sif.low,sif.close):
        if dt != pred:
            pred = dt
            curh = h
            curl = l
            icurh = ii
            icurl = ii
        else:
            if h > curh:
                curh = h
                curhl = l
                icurh = ii
                cc = c
            if l < curl:
                curl = l
                curlh = h
                icurl = ii
                cc = c
        sh[ii] = curh
        sl[ii] = curl
        ih[ii] = icurh
        il[ii] = icurl
        shl[ii] = curhl
        slh[ii] = curlh
    sif.dhigh = sh
    sif.dlow = sl
    sif.idhigh = ih
    sif.idlow = il
    sif.dhighl = shl
    sif.dlowh = slh
 
def dpeak2(sif):
    pred = 0
    sh = np.zeros_like(sif.close)
    sl = np.zeros_like(sif.close)

    ih = np.zeros_like(sif.close)
    il = np.zeros_like(sif.close)
    curh,curl = 0,99999999
    icurh,icurl = 0,0
    for ii,dt,tt,h,l,c in zip(range(len(sif.close)),sif.date,sif.time,sif.high,sif.low,sif.close):
        if dt != pred:
            pred = dt
            curh = h
            curl = l
            icurh = ii
            icurl = ii
        else:
            if h > curh:
                curh = l        ##显著不同
                icurh = ii
            if l < curl:
                curl = h        ##显著不同. 这里得到的点是第一个最低价大于上一分钟最高价时的上一分钟最高价. 相当于暴力起涨点
                icurl = ii
        sh[ii] = curh
        sl[ii] = curl
        ih[ii] = icurh
        il[ii] = icurl
    sif.dhigh2 = sh
    sif.ih2 = ih
    sif.dlow2 = sl
    sif.idlow2 = il



def dopen(sif):
    iod = sif.date - rollx(sif.date) > 0
    ohigh = np.select([iod],[sif.high],default=0)
    olow = np.select([iod],[sif.low],default=0)    
    oopen = np.select([iod],[sif.open],default=0)
    sif.odhigh = extend2next(ohigh)
    sif.odlow = extend2next(olow)
    sif.odopen = extend2next(oopen)
    

