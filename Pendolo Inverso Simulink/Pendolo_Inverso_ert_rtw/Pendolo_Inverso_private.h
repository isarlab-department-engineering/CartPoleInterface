/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: Pendolo_Inverso_private.h
 *
 * Code generated for Simulink model 'Pendolo_Inverso'.
 *
 * Model version                  : 1.21
 * Simulink Coder version         : 24.1 (R2024a) 19-Nov-2023
 * C/C++ source code generated on : Sat Oct 26 10:09:39 2024
 *
 * Target selection: ert.tlc
 * Embedded hardware selection: Atmel->AVR
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef Pendolo_Inverso_private_h_
#define Pendolo_Inverso_private_h_
#include "rtwtypes.h"
#include "Pendolo_Inverso_types.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"

/* Private macros used by the generated code to access rtModel */
#ifndef rtmIsMajorTimeStep
#define rtmIsMajorTimeStep(rtm)        (((rtm)->Timing.simTimeStep) == MAJOR_TIME_STEP)
#endif

#ifndef rtmIsMinorTimeStep
#define rtmIsMinorTimeStep(rtm)        (((rtm)->Timing.simTimeStep) == MINOR_TIME_STEP)
#endif

#ifndef rtmSetTPtr
#define rtmSetTPtr(rtm, val)           ((rtm)->Timing.t = (val))
#endif

/* Used by FromWorkspace Block: '<S13>/From Workspace' */
#ifndef rtInterpolate
# define rtInterpolate(v1,v2,f1,f2)    (((v1)==(v2))?((double)(v1)): (((f1)*((double)(v1)))+((f2)*((double)(v2)))))
#endif

#ifndef rtRound
# define rtRound(v)                    ( ((v) >= 0) ? floor((v) + 0.5) : ceil((v) - 0.5) )
#endif

#ifdef __cplusplus
#define SFB_EXTERN_C                   extern "C"
#else
#define SFB_EXTERN_C                   extern
#endif

SFB_EXTERN_C void sfcn_encoder_Start_wrapper(real_T *xD,
  const uint8_T *enc, const int_T p_width0,
  const uint8_T *pinA, const int_T p_width1,
  const uint8_T *pinB, const int_T p_width2);
SFB_EXTERN_C void sfcn_encoder_Outputs_wrapper(int16_T *pos,
  const real_T *xD,
  const uint8_T *enc, const int_T p_width0,
  const uint8_T *pinA, const int_T p_width1,
  const uint8_T *pinB, const int_T p_width2);
SFB_EXTERN_C void sfcn_encoder_Update_wrapper(int16_T *pos,
  real_T *xD,
  const uint8_T *enc, const int_T p_width0,
  const uint8_T *pinA, const int_T p_width1,
  const uint8_T *pinB, const int_T p_width2);
SFB_EXTERN_C void sfcn_encoder_Terminate_wrapper(real_T *xD,
  const uint8_T *enc, const int_T p_width0,
  const uint8_T *pinA, const int_T p_width1,
  const uint8_T *pinB, const int_T p_width2);

#undef SFB_EXTERN_C
#ifdef __cplusplus
#define SFB_EXTERN_C                   extern "C"
#else
#define SFB_EXTERN_C                   extern
#endif

SFB_EXTERN_C void sfcn_toPins_Start_wrapper(void);
SFB_EXTERN_C void sfcn_toPins_Outputs_wrapper(const real_T *Enable,
  const real_T *Analog,
  const real_T *torqueOut,
  const real_T *Mode,
  const real_T *cartPos,
  const real_T *Input,
  real_T *EnableOut,
  real_T *Dir,
  real_T *PWMOut);
SFB_EXTERN_C void sfcn_toPins_Terminate_wrapper(void);

#undef SFB_EXTERN_C

extern real_T rt_roundd_snf(real_T u);

#endif                                 /* Pendolo_Inverso_private_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
