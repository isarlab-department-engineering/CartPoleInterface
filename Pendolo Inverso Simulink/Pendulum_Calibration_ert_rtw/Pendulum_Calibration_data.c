/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * File: Pendulum_Calibration_data.c
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

/* Block parameters (default storage) */
P_Pendulum_Calibration_T Pendulum_Calibration_P = {
  /* Expression: 0.05
   * Referenced by: '<Root>/Analog Input1'
   */
  0.05,

  /* Expression: 511.5
   * Referenced by: '<S2>/Constant1'
   */
  511.5,

  /* Expression: 360
   * Referenced by: '<S2>/Constant'
   */
  360.0,

  /* Expression: 0
   * Referenced by:
   */
  0.0,

  /* Expression: 5
   * Referenced by: '<S2>/RodOffset'
   */
  5.0,

  /* Computed Parameter: DiscreteZeroPole2_A
   * Referenced by: '<Root>/Discrete Zero-Pole2'
   */
  0.86070797642505781,

  /* Computed Parameter: DiscreteZeroPole2_C
   * Referenced by: '<Root>/Discrete Zero-Pole2'
   */
  0.12910619646375868,

  /* Computed Parameter: DiscreteZeroPole2_D
   * Referenced by: '<Root>/Discrete Zero-Pole2'
   */
  0.075
};

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
