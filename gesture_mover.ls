/PROG  GESTURE_MOVER
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "Move fanuc with gestures";
PROG_SIZE	= 258;
CREATE		= DATE 23-06-27  TIME 19:14:34;
MODIFIED	= DATE 23-06-27  TIME 19:14:34;
FILE_NAME	= KAREL_MO;
VERSION		= 0;
LINE_COUNT	= 5;
MEMORY_SIZE	= 750;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
/APPL
/MN
   1:  UFRAME_NUM=2 ;
   2:  RUN GESTURE ;
   3:  LBL[1] ;
   4:J PR[1] 60% CNT10    ;
   5:  JMP LBL[1] ;
/POS
/END
