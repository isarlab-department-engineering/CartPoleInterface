/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: Pendulum_Calibration_types.h
 *
 * Code generated for Simulink model 'Pendulum_Calibration'.
 *
 * Model version                  : 1.1
 * Simulink Coder version         : 24.1 (R2024a) 19-Nov-2023
 * C/C++ source code generated on : Fri Oct 11 10:22:27 2024
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: Atmel->AVR
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef Pendulum_Calibration_types_h_
#define Pendulum_Calibration_types_h_
#include "MW_SVD.h"
#include "rtwtypes.h"

/* Custom Type definition for MATLABSystem: '<Root>/Analog Input1' */
#include "MW_SVD.h"
#ifndef struct_tag_UTG5XI0vJCsmjbgura8BP
#define struct_tag_UTG5XI0vJCsmjbgura8BP

struct tag_UTG5XI0vJCsmjbgura8BP
{
  MW_Handle_Type MW_ANALOGIN_HANDLE;
};

#endif                                 /* struct_tag_UTG5XI0vJCsmjbgura8BP */

#ifndef typedef_g_arduinodriver_ArduinoAnalog_T
#define typedef_g_arduinodriver_ArduinoAnalog_T

typedef struct tag_UTG5XI0vJCsmjbgura8BP g_arduinodriver_ArduinoAnalog_T;

#endif                             /* typedef_g_arduinodriver_ArduinoAnalog_T */

#ifndef struct_tag_8ohiN1FAOgR98njPNu14NC
#define struct_tag_8ohiN1FAOgR98njPNu14NC

struct tag_8ohiN1FAOgR98njPNu14NC
{
  boolean_T matlabCodegenIsDeleted;
  int32_T isInitialized;
  boolean_T isSetupComplete;
  g_arduinodriver_ArduinoAnalog_T AnalogInDriverObj;
  real_T SampleTime;
};

#endif                                 /* struct_tag_8ohiN1FAOgR98njPNu14NC */

#ifndef typedef_codertarget_arduinobase_inter_T
#define typedef_codertarget_arduinobase_inter_T

typedef struct tag_8ohiN1FAOgR98njPNu14NC codertarget_arduinobase_inter_T;

#endif                             /* typedef_codertarget_arduinobase_inter_T */

/* Parameters (default storage) */
typedef struct P_Pendulum_Calibration_T_ P_Pendulum_Calibration_T;

/* Forward declaration for rtModel */
typedef struct tag_RTM_Pendulum_Calibration_T RT_MODEL_Pendulum_Calibration_T;

#endif                                 /* Pendulum_Calibration_types_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
