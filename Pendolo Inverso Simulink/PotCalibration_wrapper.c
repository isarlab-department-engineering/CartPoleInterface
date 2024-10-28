
/*
 * Include Files
 *
 */
#if defined(MATLAB_MEX_FILE)
#include "tmwtypes.h"
#include "simstruc_types.h"
#else
#define SIMPLIFIED_RTWTYPES_COMPATIBILITY
#include "rtwtypes.h"
#undef SIMPLIFIED_RTWTYPES_COMPATIBILITY
#endif



/* %%%-SFUNWIZ_wrapper_includes_Changes_BEGIN --- EDIT HERE TO _END */
#include <math.h>

int maxAnalog = 0;
int minAnalog = 1023;
/* %%%-SFUNWIZ_wrapper_includes_Changes_END --- EDIT HERE TO _BEGIN */
#define u_width 1
#define u_1_width 1
#define y_width 1
#define y_1_width 1
#define y_2_width 1

/*
 * Create external references here.  
 *
 */
/* %%%-SFUNWIZ_wrapper_externs_Changes_BEGIN --- EDIT HERE TO _END */
/* extern double func(double a); */
/* %%%-SFUNWIZ_wrapper_externs_Changes_END --- EDIT HERE TO _BEGIN */

/*
 * Output function
 *
 */
void PotCalibration_Outputs_wrapper(const real_T *Analog,
			const real_T *Save,
			real_T *maxValue,
			real_T *minValue,
			real_T *initialValue)
{
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_BEGIN --- EDIT HERE TO _END */
if (Analog[0]>maxAnalog){
    maxAnalog=Analog[0];}
if (minAnalog > Analog[0]){
    minAnalog=Analog[0];}
if (Save[0]==1){
    maxValue[0]=maxAnalog;
    minValue[0]=minAnalog;
    initialValue[0]=Analog[0];
}else{
    maxValue[0]=0;
    minValue[0]=0;
    initialValue[0]=0;}
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_END --- EDIT HERE TO _BEGIN */
}


