## **Cautionary Statement:**

*This collection comprises a set of unrefined scripts for activating/deactivating resource parking toggles. It is advised to exercise discretion when reviewing the code if one experiences significant Obsessive-Compulsive Disorder tendencies.*

## How to Run?

  
**setup AWS env**

    export AWS_PROFILE=dev

**to disable schedulers**

    python3 setRDSTags.py dev false
    
    python3 disableASGSchedulers.py dev
    
    python3 toggle_triggers.py dev disable

**to enable schedulers**

    python3 setRDSTags.py dev true
    
    python3 enableASGSchedulers.py dev
    
    python3 toggle_triggers.py dev enable
