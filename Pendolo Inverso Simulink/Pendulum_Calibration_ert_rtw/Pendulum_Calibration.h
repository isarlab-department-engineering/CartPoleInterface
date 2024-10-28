/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: Pendulum_Calibration.h
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

#ifndef Pendulum_Calibration_h_
#define Pendulum_Calibration_h_
#ifndef Pendulum_Calibration_COMMON_INCLUDES_
#define Pendulum_Calibration_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_extmode.h"
#include "sysran_types.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#include "MW_AnalogIn.h"
#endif                               /* Pendulum_Calibration_COMMON_INCLUDES_ */

#include "Pendulum_Calibration_types.h"
#include <math.h>
#include "MW_target_hardware_resources.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetFinalTime
#define rtmGetFinalTime(rtm)           ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetRTWExtModeInfo
#define rtmGetRTWExtModeInfo(rtm)      ((rtm)->extModeInfo)
#endif

#ifndef rtmGetErrorStatus
#define rtmGetErrorStatus(rtm)         ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
#define rtmSetErrorStatus(rtm, val)    ((rtm)->errorStatus = (val))
#endif

#ifndef rtmStepTask
#define rtmStepTask(rtm, idx)          ((rtm)->Timing.TaskCounters.TID[(idx)] == 0)
#endif

#ifndef rtmGetStopRequested
#define rtmGetStopRequested(rtm)       ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
#define rtmSetStopRequested(rtm, val)  ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
#define rtmGetStopRequestedPtr(rtm)    (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
#define rtmGetT(rtm)                   (rtmGetTPtr((rtm))[0])
#endif

#ifndef rtmGetTFinal
#define rtmGetTFinal(rtm)              ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetTPtr
#define rtmGetTPtr(rtm)                ((rtm)->Timing.t)
#endif

#ifndef rtmTaskCounter
#define rtmTaskCounter(rtm, idx)       ((rtm)->Timing.TaskCounters.TID[(idx)])
#endif

/* Block signals (default storage) */
typedef struct {
  real_T FromWorkspace[3];             /* '<S2>/From Workspace' */
  real_T TmpRTBAtDivide3Inport1;
  real_T Divide3;                      /* '<S2>/Divide3' */
  real_T Merge;                        /* '<S2>/Merge' */
  real_T Divide1;                      /* '<S2>/Divide1' */
  real_T Subtract1;                    /* '<S2>/Subtract1' */
  real_T DiscreteZeroPole2;            /* '<Root>/Discrete Zero-Pole2' */
  real_T DataTypeConversion1;          /* '<Root>/Data Type Conversion1' */
} B_Pendulum_Calibration_T;

/* Block states (default storage) for system '<Root>' */
typedef struct {
  codertarget_arduinobase_inter_T obj; /* '<Root>/Analog Input1' */
  real_T DiscreteZeroPole2_DSTATE;     /* '<Root>/Discrete Zero-Pole2' */
  real_T TmpRTBAtDivide3Inport1_Buffer0;/* synthesized block */
  struct {
    void *TimePtr;
    void *DataPtr;
    void *RSimInfoPtr;
  } FromWorkspace_PWORK;               /* '<S2>/From Workspace' */

  struct {
    void *LoggedData;
  } Scope_PWORK;                       /* '<Root>/Scope' */

  struct {
    int_T PrevIndex;
  } FromWorkspace_IWORK;               /* '<S2>/From Workspace' */

  int8_T IfActionSubsystem1_SubsysRanBC;/* '<S2>/If Action Subsystem1' */
  int8_T IfActionSubsystem_SubsysRanBC;/* '<S2>/If Action Subsystem' */
} DW_Pendulum_Calibration_T;

/* External outputs (root outports fed by signals with default storage) */
typedef struct {
  real_T Analog;                       /* '<Root>/Analog' */
  real_T Theta;                        /* '<Root>/Theta°' */
} ExtY_Pendulum_Calibration_T;

/* Parameters (default storage) */
struct P_Pendulum_Calibration_T_ {
  real_T AnalogInput1_SampleTime;      /* Expression: 0.05
                                        * Referenced by: '<Root>/Analog Input1'
                                        */
  real_T Constant1_Value;              /* Expression: 511.5
                                        * Referenced by: '<S2>/Constant1'
                                        */
  real_T Constant_Value;               /* Expression: 360
                                        * Referenced by: '<S2>/Constant'
                                        */
  real_T TmpRTBAtDivide3Inport1_InitialC;/* Expression: 0
                                          * Referenced by:
                                          */
  real_T RodOffset_Value;              /* Expression: 5
                                        * Referenced by: '<S2>/RodOffset'
                                        */
  real_T DiscreteZeroPole2_A;         /* Computed Parameter: DiscreteZeroPole2_A
                                       * Referenced by: '<Root>/Discrete Zero-Pole2'
                                       */
  real_T DiscreteZeroPole2_C;         /* Computed Parameter: DiscreteZeroPole2_C
                                       * Referenced by: '<Root>/Discrete Zero-Pole2'
                                       */
  real_T DiscreteZeroPole2_D;         /* Computed Parameter: DiscreteZeroPole2_D
                                       * Referenced by: '<Root>/Discrete Zero-Pole2'
                                       */
};

/* Real-time Model Data Structure */
struct tag_RTM_Pendulum_Calibration_T {
  const char_T *errorStatus;
  RTWExtModeInfo *extModeInfo;
  RTWSolverInfo solverInfo;

  /*
   * Sizes:
   * The following substructure contains sizes information
   * for many of the model attributes such as inputs, outputs,
   * dwork, sample times, etc.
   */
  struct {
    uint32_T checksums[4];
  } Sizes;

  /*
   * SpecialInfo:
   * The following substructure contains special information
   * related to other components that are dependent on RTW.
   */
  struct {
    const void *mappingInfo;
  } SpecialInfo;

  /*
   * Timing:
   * The following substructure contains information regarding
   * the timing information for the model.
   */
  struct {
    uint32_T clockTick0;
    time_T stepSize0;
    uint32_T clockTick1;
    uint32_T clockTick2;
    struct {
      uint8_T TID[3];
    } TaskCounters;

    struct {
      boolean_T TID1_2;
    } RateInteraction;

    time_T tFinal;
    SimTimeStep simTimeStep;
    boolean_T stopRequestedFlag;
    time_T *t;
    time_T tArray[3];
  } Timing;
};

/* Block parameters (default storage) */
extern P_Pendulum_Calibration_T Pendulum_Calibration_P;

/* Block signals (default storage) */
extern B_Pendulum_Calibration_T Pendulum_Calibration_B;

/* Block states (default storage) */
extern DW_Pendulum_Calibration_T Pendulum_Calibration_DW;

/* External outputs (root outports fed by signals with default storage) */
extern ExtY_Pendulum_Calibration_T Pendulum_Calibration_Y;

/* External function called from main */
extern void Pendulum_Calibration_SetEventsForThisBaseStep(boolean_T *eventFlags);

/* Model entry point functions */
extern void Pendulum_Calibration_initialize(void);
extern void Pendulum_Calibration_step0(void);
extern void Pendulum_Calibration_step2(void);
extern void Pendulum_Calibration_terminate(void);

/* Real-time Model object */
extern RT_MODEL_Pendulum_Calibration_T *const Pendulum_Calibration_M;
extern volatile boolean_T stopRequested;
extern volatile boolean_T runModel;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'Pendulum_Calibration'
 * '<S1>'   : 'Pendulum_Calibration/Convert1'
 * '<S2>'   : 'Pendulum_Calibration/Convert1/Analog to Angle'
 * '<S3>'   : 'Pendulum_Calibration/Convert1/Analog to Angle/If Action Subsystem'
 * '<S4>'   : 'Pendulum_Calibration/Convert1/Analog to Angle/If Action Subsystem1'
 */
#endif                                 /* Pendulum_Calibration_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
