/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: Pendulum_Calibration.c
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

#include "Pendulum_Calibration.h"
#include "rtwtypes.h"
#include "Pendulum_Calibration_private.h"

/* Block signals (default storage) */
B_Pendulum_Calibration_T Pendulum_Calibration_B;

/* Block states (default storage) */
DW_Pendulum_Calibration_T Pendulum_Calibration_DW;

/* External outputs (root outports fed by signals with default storage) */
ExtY_Pendulum_Calibration_T Pendulum_Calibration_Y;

/* Real-time model */
static RT_MODEL_Pendulum_Calibration_T Pendulum_Calibration_M_;
RT_MODEL_Pendulum_Calibration_T *const Pendulum_Calibration_M =
  &Pendulum_Calibration_M_;
static void rate_monotonic_scheduler(void);

/*
 * Set which subrates need to run this base step (base rate always runs).
 * This function must be called prior to calling the model step function
 * in order to remember which rates need to run this base step.  The
 * buffering of events allows for overlapping preemption.
 */
void Pendulum_Calibration_SetEventsForThisBaseStep(boolean_T *eventFlags)
{
  /* Task runs when its counter is zero, computed via rtmStepTask macro */
  eventFlags[2] = ((boolean_T)rtmStepTask(Pendulum_Calibration_M, 2));
}

/*
 *         This function updates active task flag for each subrate
 *         and rate transition flags for tasks that exchange data.
 *         The function assumes rate-monotonic multitasking scheduler.
 *         The function must be called at model base rate so that
 *         the generated code self-manages all its subrates and rate
 *         transition flags.
 */
static void rate_monotonic_scheduler(void)
{
  /* To ensure a deterministic data transfer between two rates,
   * data is transferred at the priority of a fast task and the frequency
   * of the slow task.  The following flags indicate when the data transfer
   * happens.  That is, a rate interaction flag is set true when both rates
   * will run, and false otherwise.
   */

  /* tid 1 shares data with slower tid rate: 2 */
  if (Pendulum_Calibration_M->Timing.TaskCounters.TID[1] == 0) {
    Pendulum_Calibration_M->Timing.RateInteraction.TID1_2 =
      (Pendulum_Calibration_M->Timing.TaskCounters.TID[2] == 0);
  }

  /* Compute which subrates run during the next base time step.  Subrates
   * are an integer multiple of the base rate counter.  Therefore, the subtask
   * counter is reset when it reaches its limit (zero means run).
   */
  (Pendulum_Calibration_M->Timing.TaskCounters.TID[2])++;
  if ((Pendulum_Calibration_M->Timing.TaskCounters.TID[2]) > 4) {/* Sample time: [0.05s, 0.0s] */
    Pendulum_Calibration_M->Timing.TaskCounters.TID[2] = 0;
  }
}

/* Model step function for TID0 */
void Pendulum_Calibration_step0(void)  /* Sample time: [0.0s, 0.0s] */
{
  real_T rtb_Divide;

  {                                    /* Sample time: [0.0s, 0.0s] */
    rate_monotonic_scheduler();
  }

  /* Reset subsysRan breadcrumbs */
  srClearBC(Pendulum_Calibration_DW.IfActionSubsystem_SubsysRanBC);

  /* Reset subsysRan breadcrumbs */
  srClearBC(Pendulum_Calibration_DW.IfActionSubsystem1_SubsysRanBC);

  /* FromWorkspace: '<S2>/From Workspace' */
  {
    real_T *pDataValues = (real_T *)
      Pendulum_Calibration_DW.FromWorkspace_PWORK.DataPtr;

    {
      int_T elIdx;
      for (elIdx = 0; elIdx < 3; ++elIdx) {
        (&Pendulum_Calibration_B.FromWorkspace[0])[elIdx] = pDataValues[0];
        pDataValues += 1;
      }
    }
  }

  /* If: '<S2>/If' */
  if (Pendulum_Calibration_B.FromWorkspace[2] < 511.5) {
    /* Outputs for IfAction SubSystem: '<S2>/If Action Subsystem' incorporates:
     *  ActionPort: '<S3>/Action Port'
     */
    /* Merge: '<S2>/Merge' incorporates:
     *  Constant: '<S2>/Constant1'
     *  Sum: '<S3>/Sum'
     */
    Pendulum_Calibration_B.Merge = Pendulum_Calibration_B.FromWorkspace[2] +
      Pendulum_Calibration_P.Constant1_Value;
    srUpdateBC(Pendulum_Calibration_DW.IfActionSubsystem_SubsysRanBC);

    /* End of Outputs for SubSystem: '<S2>/If Action Subsystem' */
  } else {
    /* Outputs for IfAction SubSystem: '<S2>/If Action Subsystem1' incorporates:
     *  ActionPort: '<S4>/Action Port'
     */
    /* Merge: '<S2>/Merge' incorporates:
     *  Constant: '<S2>/Constant1'
     *  Sum: '<S4>/Sum'
     */
    Pendulum_Calibration_B.Merge = Pendulum_Calibration_B.FromWorkspace[2] -
      Pendulum_Calibration_P.Constant1_Value;
    srUpdateBC(Pendulum_Calibration_DW.IfActionSubsystem1_SubsysRanBC);

    /* End of Outputs for SubSystem: '<S2>/If Action Subsystem1' */
  }

  /* End of If: '<S2>/If' */
  /* Product: '<S2>/Divide' incorporates:
   *  Constant: '<S2>/Constant'
   *  Sum: '<S2>/Subtract'
   */
  rtb_Divide = (Pendulum_Calibration_B.FromWorkspace[0] -
                Pendulum_Calibration_B.FromWorkspace[1]) /
    Pendulum_Calibration_P.Constant_Value;

  /* RateTransition generated from: '<S2>/Divide3' */
  if (Pendulum_Calibration_M->Timing.RateInteraction.TID1_2) {
    /* RateTransition generated from: '<S2>/Divide3' */
    Pendulum_Calibration_B.TmpRTBAtDivide3Inport1 =
      Pendulum_Calibration_DW.TmpRTBAtDivide3Inport1_Buffer0;
  }

  /* End of RateTransition generated from: '<S2>/Divide3' */

  /* Product: '<S2>/Divide3' */
  Pendulum_Calibration_B.Divide3 = Pendulum_Calibration_B.TmpRTBAtDivide3Inport1
    / rtb_Divide;

  /* Product: '<S2>/Divide1' incorporates:
   *  Constant: '<S2>/RodOffset'
   *  Sum: '<S2>/Sum'
   */
  Pendulum_Calibration_B.Divide1 = (Pendulum_Calibration_P.RodOffset_Value +
    Pendulum_Calibration_B.Merge) / rtb_Divide;

  /* Sum: '<S2>/Subtract1' */
  Pendulum_Calibration_B.Subtract1 = Pendulum_Calibration_B.Divide3 -
    Pendulum_Calibration_B.Divide1;

  /* DiscreteZeroPole: '<Root>/Discrete Zero-Pole2' */
  {
    Pendulum_Calibration_B.DiscreteZeroPole2 =
      Pendulum_Calibration_P.DiscreteZeroPole2_D*
      Pendulum_Calibration_B.Subtract1;
    Pendulum_Calibration_B.DiscreteZeroPole2 +=
      Pendulum_Calibration_P.DiscreteZeroPole2_C*
      Pendulum_Calibration_DW.DiscreteZeroPole2_DSTATE;
  }

  /* Outport: '<Root>/Theta°' */
  Pendulum_Calibration_Y.Theta = Pendulum_Calibration_B.DiscreteZeroPole2;

  /* Update for DiscreteZeroPole: '<Root>/Discrete Zero-Pole2' */
  {
    Pendulum_Calibration_DW.DiscreteZeroPole2_DSTATE =
      Pendulum_Calibration_B.Subtract1 +
      Pendulum_Calibration_P.DiscreteZeroPole2_A*
      Pendulum_Calibration_DW.DiscreteZeroPole2_DSTATE;
  }

  /* Update absolute time */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   */
  Pendulum_Calibration_M->Timing.t[0] =
    ((time_T)(++Pendulum_Calibration_M->Timing.clockTick0)) *
    Pendulum_Calibration_M->Timing.stepSize0;

  /* Update absolute time */
  /* The "clockTick1" counts the number of times the code of this task has
   * been executed. The resolution of this integer timer is 0.01, which is the step size
   * of the task. Size of "clockTick1" ensures timer will not overflow during the
   * application lifespan selected.
   */
  Pendulum_Calibration_M->Timing.clockTick1++;
}

/* Model step function for TID2 */
void Pendulum_Calibration_step2(void)  /* Sample time: [0.05s, 0.0s] */
{
  uint16_T b_varargout_1;

  /* MATLABSystem: '<Root>/Analog Input1' */
  if (Pendulum_Calibration_DW.obj.SampleTime !=
      Pendulum_Calibration_P.AnalogInput1_SampleTime) {
    Pendulum_Calibration_DW.obj.SampleTime =
      Pendulum_Calibration_P.AnalogInput1_SampleTime;
  }

  Pendulum_Calibration_DW.obj.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
    MW_AnalogIn_GetHandle(59UL);
  MW_AnalogInSingle_ReadResult
    (Pendulum_Calibration_DW.obj.AnalogInDriverObj.MW_ANALOGIN_HANDLE,
     &b_varargout_1, MW_ANALOGIN_UINT16);

  /* DataTypeConversion: '<Root>/Data Type Conversion1' incorporates:
   *  MATLABSystem: '<Root>/Analog Input1'
   * */
  Pendulum_Calibration_B.DataTypeConversion1 = b_varargout_1;

  /* Outport: '<Root>/Analog' */
  Pendulum_Calibration_Y.Analog = Pendulum_Calibration_B.DataTypeConversion1;

  /* RateTransition generated from: '<S2>/Divide3' */
  Pendulum_Calibration_DW.TmpRTBAtDivide3Inport1_Buffer0 =
    Pendulum_Calibration_B.DataTypeConversion1;

  /* Update absolute time */
  /* The "clockTick2" counts the number of times the code of this task has
   * been executed. The resolution of this integer timer is 0.05, which is the step size
   * of the task. Size of "clockTick2" ensures timer will not overflow during the
   * application lifespan selected.
   */
  Pendulum_Calibration_M->Timing.clockTick2++;
}

/* Model initialize function */
void Pendulum_Calibration_initialize(void)
{
  /* Registration code */
  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&Pendulum_Calibration_M->solverInfo,
                          &Pendulum_Calibration_M->Timing.simTimeStep);
    rtsiSetTPtr(&Pendulum_Calibration_M->solverInfo, &rtmGetTPtr
                (Pendulum_Calibration_M));
    rtsiSetStepSizePtr(&Pendulum_Calibration_M->solverInfo,
                       &Pendulum_Calibration_M->Timing.stepSize0);
    rtsiSetErrorStatusPtr(&Pendulum_Calibration_M->solverInfo,
                          (&rtmGetErrorStatus(Pendulum_Calibration_M)));
    rtsiSetRTModelPtr(&Pendulum_Calibration_M->solverInfo,
                      Pendulum_Calibration_M);
  }

  rtsiSetSimTimeStep(&Pendulum_Calibration_M->solverInfo, MAJOR_TIME_STEP);
  rtsiSetIsMinorTimeStepWithModeChange(&Pendulum_Calibration_M->solverInfo,
    false);
  rtsiSetIsContModeFrozen(&Pendulum_Calibration_M->solverInfo, false);
  rtsiSetSolverName(&Pendulum_Calibration_M->solverInfo,"FixedStepDiscrete");
  rtmSetTPtr(Pendulum_Calibration_M, &Pendulum_Calibration_M->Timing.tArray[0]);
  rtmSetTFinal(Pendulum_Calibration_M, -1);
  Pendulum_Calibration_M->Timing.stepSize0 = 0.01;

  /* External mode info */
  Pendulum_Calibration_M->Sizes.checksums[0] = (2578712699U);
  Pendulum_Calibration_M->Sizes.checksums[1] = (3742333080U);
  Pendulum_Calibration_M->Sizes.checksums[2] = (2211768047U);
  Pendulum_Calibration_M->Sizes.checksums[3] = (3587453227U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[4];
    Pendulum_Calibration_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = &rtAlwaysEnabled;
    systemRan[2] = (sysRanDType *)
      &Pendulum_Calibration_DW.IfActionSubsystem_SubsysRanBC;
    systemRan[3] = (sysRanDType *)
      &Pendulum_Calibration_DW.IfActionSubsystem1_SubsysRanBC;
    rteiSetModelMappingInfoPtr(Pendulum_Calibration_M->extModeInfo,
      &Pendulum_Calibration_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(Pendulum_Calibration_M->extModeInfo,
                        Pendulum_Calibration_M->Sizes.checksums);
    rteiSetTPtr(Pendulum_Calibration_M->extModeInfo, rtmGetTPtr
                (Pendulum_Calibration_M));
  }

  /* Start for FromWorkspace: '<S2>/From Workspace' */
  {
    static real_T pTimeValues0[] = { 0.0 } ;

    static real_T pDataValues0[] = { 1023.0, 3.0, 91.0 } ;

    Pendulum_Calibration_DW.FromWorkspace_PWORK.TimePtr = (void *) pTimeValues0;
    Pendulum_Calibration_DW.FromWorkspace_PWORK.DataPtr = (void *) pDataValues0;
    Pendulum_Calibration_DW.FromWorkspace_IWORK.PrevIndex = 0;
  }

  /* Start for RateTransition generated from: '<S2>/Divide3' */
  Pendulum_Calibration_B.TmpRTBAtDivide3Inport1 =
    Pendulum_Calibration_P.TmpRTBAtDivide3Inport1_InitialC;

  /* InitializeConditions for RateTransition generated from: '<S2>/Divide3' */
  Pendulum_Calibration_DW.TmpRTBAtDivide3Inport1_Buffer0 =
    Pendulum_Calibration_P.TmpRTBAtDivide3Inport1_InitialC;

  /* Start for MATLABSystem: '<Root>/Analog Input1' */
  Pendulum_Calibration_DW.obj.matlabCodegenIsDeleted = false;
  Pendulum_Calibration_DW.obj.SampleTime =
    Pendulum_Calibration_P.AnalogInput1_SampleTime;
  Pendulum_Calibration_DW.obj.isInitialized = 1L;
  Pendulum_Calibration_DW.obj.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
    MW_AnalogInSingle_Open(59UL);
  Pendulum_Calibration_DW.obj.isSetupComplete = true;
}

/* Model terminate function */
void Pendulum_Calibration_terminate(void)
{
  /* Terminate for MATLABSystem: '<Root>/Analog Input1' */
  if (!Pendulum_Calibration_DW.obj.matlabCodegenIsDeleted) {
    Pendulum_Calibration_DW.obj.matlabCodegenIsDeleted = true;
    if ((Pendulum_Calibration_DW.obj.isInitialized == 1L) &&
        Pendulum_Calibration_DW.obj.isSetupComplete) {
      Pendulum_Calibration_DW.obj.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
        MW_AnalogIn_GetHandle(59UL);
      MW_AnalogIn_Close
        (Pendulum_Calibration_DW.obj.AnalogInDriverObj.MW_ANALOGIN_HANDLE);
    }
  }

  /* End of Terminate for MATLABSystem: '<Root>/Analog Input1' */
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
