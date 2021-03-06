import os
import sys
import numpy as np
import argparse
import subprocess
import json
import time
from scipy.ndimage import gaussian_filter1d
import nibabel as nib
import brainsss
import gc

def main(args):

    logfile = args['logfile']
    directory = args['directory'] # full fly func path
    smooth = args['smooth']
    colors = args['colors']
    printlog = getattr(brainsss.Printlog(logfile=logfile), 'print_to_log')

    #['red', 'green']
    printlog('colors are: {}'.format(colors))
    for color in colors:
        brain_file = os.path.join(directory, 'moco', 'moco_stitched_brain_{}.nii'.format(color))
        if os.path.exists(brain_file):
            t0 = time.time()
            to_print = '/'.join(brain_file.split('/')[-4:])
            printlog(f'Z-scoring{to_print:.>{120-9}}')

            brain = np.asarray(nib.load(brain_file).get_data(), dtype='uint16')

            printlog("brain load duration: ({})".format(time.time()-t0))
            # t0 = time.time()
            printlog('smooth is {}'.format(smooth))
            if smooth:
                printlog('smoothing')
                smoothed = gaussian_filter1d(brain,sigma=200,axis=-1,truncate=1)
                printlog("brain smoothed duration: ({})".format(time.time()-t0))
                t0 = time.time()
                brain = brain - smoothed
                printlog("brain subtracted duration: ({})".format(time.time()-t0))
                t0 = time.time()
                zbrain_file = os.path.join(directory, 'brain_zscored_{}_smooth.nii'.format(color))
            else:
                printlog('not smoothing')
                zbrain_file = os.path.join(directory, 'brain_zscored_{}.nii'.format(color))

            # Z-score brain
            brain_mean  = np.mean(brain, axis=3)

            printlog("brain mean duration: ({})".format(time.time()-t0))
            # t0 = time.time()

            brain_std = np.std(brain, axis=3)

            printlog("brain std duration: ({})".format(time.time()-t0))
            # t0 = time.time()

            #brain = (brain - brain_mean[:,:,:,None]) / brain_std[:,:,:,None]
            #luke suggestion to reduce memory usage
            for z in range(brain.shape[-2]):  #I think this should iterate over slice z for [x,y,z,none] https://stackoverflow.com/questions/1589706/iterating-over-arbitrary-dimension-of-numpy-array
                #brain[:,:,z,None] = (brain[:,:,z,None] - brain_mean[:,:,z,None]) / brain_std[:,:,z,None]
                
                #may be this because brain should have a time dimension, but not sure about it...
                brain[:,:,z,:] = (brain[:,:,z,:] - brain_mean[:,:,z,None]) / brain_std[:,:,z,None]

                
                
            printlog("brain zscored duration: ({})".format(time.time()-t0))
            # t0 = time.time()

            # Save brain
            
            printlog('Saving {}'.format(zbrain_file))
            aff = np.eye(4)
            img = nib.Nifti1Image(brain, aff)
            img.to_filename(zbrain_file)

            printlog("brain save duration: ({})".format(time.time()-t0))
            
            del zbrain_file  #to delete from memory
            del brain # to delete from memory
            del brain_std
            del brain_mean
            gc.collect()  #extra delete from memory
            printlog("deleting brains from memory")

if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
