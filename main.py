import time
import logging
import logging.handlers

def log_setup():
    log_handler = logging.handlers.RotatingFileHandler('my.log', maxBytes=5*1000*1000, backupCount=10)
    formatter = logging.Formatter(
        '%(asctime)s program_name [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

log_setup()


import os
from datetime import datetime as dt
start_t=dt.now()
clear = lambda: os.system('cls') #on Windows System


M=[0]*81

O_hor=[
  '|', '|', '|', '|', '|', '|', '|', '|',
  '|', '|', '|', '*', '|', '|', '|', '|',
  '|', '|', '|', '*', '*', '*', '|', '|',
  '|', '|', '|', '|', '|', '*', '|', '|',
  '|', '*', '|', '|', '|', '|', '|', '*',
  '|', '|', '+', '*', '|', '*', '*', '|',
  '|', '|', '|', '*', '|', '|', '|', '|',
  '|', '|', '*', '|', '|', '|', '|', '|',
  '*', '+', '|', '|', '|', '|', '*', '|']
O_ver=[
  '*', '|', '|', '+', '+', '+', '|', '|', '|',
  '|', '|', '|', '|', '|', '*', '|', '|', '|',
  '|', '|', '+', '|', '*', '|', '|', '|', '|',
  '|', '|', '|', '|', '+', '+', '|', '*', '*',
  '+', '|', '+', '|', '|', '+', '|', '*', '|',
  '|', '|', '|', '*', '*', '+', '*', '|', '+',
  '*', '|', '|', '|', '|', '|', '|', '|', '|',
  '*', '|', '|', '|', '|', '|', '|', '|', '|']

def pprint_M():
  S='/'*18
  for i in range(8):    
    m=M[i*9:i*9+9]
    o=O_hor[i*8:i*8+8]
    s1=str(m[0])
    for j in range(8):
      s1+=o[j]+str(m[j+1])
    o=O_ver[i*9:i*9+9]
    s2=''
    for j in range(9):
      o[j]='-' if o[j]=='|' else o[j]
      s2+=o[j]+' '
    S=S+'\n'+s1
    S=S+'\n'+s2
  i=8
  m=M[i*9:i*9+9]
  o=O_hor[i*8:i*8+8]
  s1=str(m[0])
  for j in range(8):
    s1+=o[j]+str(m[j+1])
  S=S+'\n'+s1
  S=S+'\n'+'/'*18
  #print(S)
  return S

def rules(j,i):
  msg="{} not allowed at M[{}] because ".format(j,i)
  if i==12:
    #print('x')
    pass

  def add(i=i-1):
    return j!=M[i]+1
  def subtract(i=i-1):
    return j!=M[i]-1
  def multiply(i=i-1):
    return j!=2*M[i]
  def divide(i=i-1):
    return j!=M[i]/2
  def checkrow():
    s=set(M[(i//9)*9:(i//9)*9+9])
    return j not in s
  def checkcol():
    l=[(i%9)+k*9 for k in range(9)]
    s={M[k] for k in l}
    return j not in s
  row=i//9
  col=i%9
  out=True
  if not i in {i for i in range(9)}:
    #check top    
    operator_row=row-1
    operator_col=col
    operator=O_ver[operator_row*9+operator_col]
    if operator=='|':
      out&=add((row-1)*9+col) & subtract((row-1)*9+col) & multiply((row-1)*9+col) & divide((row-1)*9+col)
    if operator=='*':
      bool1=not multiply((row-1)*9+col)
      bool2=not divide((row-1)*9+col)
      out&=(bool1 | bool2)
    if operator=='+':
      bool1=not add((row-1)*9+col) 
      bool2=not subtract((row-1)*9+col)
      out&=(bool1 | bool2)
    logging.info("M[{}] ({}) is on top of M[{}] and is connected with the operator O_ver[{}]={}".format((row-1)*9+col,M[(row-1)*9+col],i,operator_row*9+operator_col,operator))
  if not i in {i*9 for i in range(9)}:
    #check left
    operator_row=row
    operator_col=col-1
    operator=O_hor[operator_row*8+operator_col]
    if operator=='|':
      out&=add(row*9+col-1) & subtract(row*9+col-1) & multiply(row*9+col-1) & divide(row*9+col-1)
    if operator=='*':
      bool1=not multiply(row*9+col-1)
      bool2=not divide(row*9+col-1)
      out&=(bool1 | bool2)
    if operator=='+':
      bool1=not add(row*9+col-1)
      bool2=not subtract(row*9+col-1)
      out&=(bool1 | bool2)
    logging.info("M[{}] ({}) is left of M[{}] and is connected with the operator O_hor[{}]={}".format(row*9+col-1,M[row*9+col-1],i,operator_row*8+operator_col,operator))


  out=out & checkcol() & checkrow()
  if out:
    logging.info('setting {} at M[{}] is allowed'.format(j,i))
  else:
    logging.info('setting {} at M[{}] is not allowed'.format(j,i))
  return out




def recu(i):
  clear()
  print(10*'-',i,10*'-')
  print((i//5)*'#',((81-i)//5)*'-')
  print(dt.now()-start_t)
  print(pprint_M())
  j=1
  while j<10:
    msg="{} not allowed at M[{}] because ".format(j,i)
    if rules(j,i):
      M[i]=j
      logging.info("setting {} at M[{}]".format(j,i))
      if recu(i+1):
        return True
      else:
        logging.info(msg+"its not working in deeper structures")
        logging.info('\n'+pprint_M())
        M[i]=0
        logging.info("setting {} at M[{}]".format(0,i))

    j+=1
  return False



recu(0)
