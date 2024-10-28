
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
# ifndef MATLAB_MEX_FILE
# include <Arduino.h>
double scale;
double controlMode=0;
bool enableIn;
bool dirIn;
double preAnalog;
double PreanalogSign;
double analogSign;
# endif
/* %%%-SFUNWIZ_wrapper_includes_Changes_END --- EDIT HERE TO _BEGIN */
#define u_width 1
#define u_1_width 1
#define u_2_width 1
#define u_3_width 1
#define u_4_width 1
#define u_5_width 1
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
void sfcn_toPins_Outputs_wrapper(const real_T *Enable,
			const real_T *Analog,
			const real_T *torqueOut,
			const real_T *Mode,
			const real_T *cartPos,
			const real_T *Input,
			real_T *EnableOut,
			real_T *Dir,
			real_T *PWMOut)
{
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_BEGIN --- EDIT HERE TO _END */
#ifndef MATLAB_MEX_FILE

if (Analog[0] < 0) {
  analogSign = -1;
} else if (Analog[0] > 0) {
  analogSign = 1;
} else {
  analogSign = 0;
}
if (Enable[0] == 1) {
  enableIn = 1;
  if (Mode[0] == 0) {
    if (torqueOut[0] <= 0) {
      scale = (-torqueOut[0] / 5.8824);
      dirIn = 1;
    } else if (torqueOut[0] > 0) {
      scale = (torqueOut[0] / 5.8824);
      dirIn = 0;
    }
  } else {
      if (((-20) <= (Analog[0]) && (Analog[0] <= 20)) &&
              (1370 >= (cartPos[0]) && (cartPos[0]) >= (-1370))) {
        if (torqueOut[0] <= 0) {
          scale = (-torqueOut[0] / 5.8824);
          dirIn = 1;
        } else if (torqueOut[0] > 0) {
          scale = (torqueOut[0] / 5.8824);
          dirIn = 0;
        }
      }else {
        enableIn = 0;
      }
  }
} else {
  controlMode = 0;
  enableIn = 0;
}
PreanalogSign = analogSign;
EnableOut[0] = enableIn;
Dir[0] = dirIn;
PWMOut[0] = scale;

#endif
/* %%%-SFUNWIZ_wrapper_Outputs_Changes_END --- EDIT HERE TO _BEGIN */
}


