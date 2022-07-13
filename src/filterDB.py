import os
import sqlalchemy as sa
import pandas as pd

from ReadMDBFiles import ReadMDBFiles


import concurrent.futures


def filterDB(params):

    fullGender = params["gender"]
    telephoneNumber = params["telephoneNumber"]
    aadharNoOfCustomer = params["addressNumber"]
    nameOfSubscriber = params["subscriberName"]
    dateOfBirthFrom = params["fromBirthDate"]
    dateOfBirthTo = params["toBirthDate"]
    fathersHusbandsName = params["fatherHusbandName"]
    permanentAddress = params["permanentAddress"]
    localAddress = params["localAddress"]
    alternatePhoneNo = params["alternateTelephoneNumber"]
    emailId = params["email"]
    statusOfSubscriber = params["subscriberStatus"]
    simActivationDateFrom = params["fromSIMActivationDate"]
    simActivationDateTo = params["toSIMActivationDate"]
    currentStatusOfConnection = params["conectionStatus"]
    useBirthDate = params["useBirthDate"]
    useSIMActivationDate = params["useSIMActivationDate"]

    DBDir = "../Data/ms access database/"

    outputFile = "../Data/query result/results.csv"

    if (os.path.exists(outputFile)):
        os.remove(outputFile)

    MDBFiles = ReadMDBFiles(DBDir)

    def readFile(fileInfo):
        fileName, filePath = fileInfo
         
        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + filePath + ";"
            r"ExtendedAnsiSQL=1;"
        )

        connection_url = sa.engine.URL.create(
            "access+pyodbc",
            query={"odbc_connect": connection_string}
        )

        engine = sa.create_engine(connection_url)

        query = """
                    SELECT
                        DATE_OF_BIRTH AS BirthDate,
                        SIM_ACTIVATION_DATE AS SIMActivationDate,
                        GENDER,
                        TELEPHONE_NUMBER AS PhoneNumber,
                        AADHAR_NO_OF_CUSTOMER AS CustomerAddress,
                        NAME_OF_SUBSCRIBER AS SubscriberName,
                        FATHERs_HUSBANDs_NAME AS FatherHusbandName,
                        PERMANENT_ADDRESS AS PermanentAddress,
                        LOCAL_ADDRESS AS LocalAddress,
                        ALTERNATE_PHONE_NO AS AlternatePhone,
                        E_MAILID AS Email,
                        STATUS_OF_SUBSCRIBER AS SubscriberStatus,
                        CURRENT_STATUS_OF_CONNECTION AS ConnectionStatus
                    FROM
                        {tableName}
                    WHERE
                        (({useBirthDateOp} = 0) 
                        OR (IsDate(DATE_OF_BIRTH) = -1 AND Format(DATE_OF_BIRTH,'yyyy-MM-dd') BETWEEN  Format('{dateOfBirthFromOp}','yyyy-MM-dd') AND Format('{dateOfBirthToOp}','yyyy-MM-dd')))
                        AND (({useSIMActivationDateOp} = 0) OR (IsDate(SIM_ACTIVATION_DATE) = -1 AND Format(SIM_ACTIVATION_DATE,'yyyy-MM-dd') BETWEEN  Format('{simActivationDateFromOp}','yyyy-MM-dd') AND Format('{simActivationDateToOp}','yyyy-MM-dd')))
                        AND ('{fullGenderOp}' = '' OR '{genderOp}' = '' OR  GENDER = '{genderOp}' OR GENDER = '{fullGenderOp}') 
                        AND ('{telephoneNumberOp}' = '' OR TELEPHONE_NUMBER like '%{telephoneNumberOp}%')
                        AND ('{aadharNoOfCustomerOp}' = '' OR AADHAR_NO_OF_CUSTOMER like '%{aadharNoOfCustomerOp}%')
                        AND ('{nameOfSubscriberOp}' = '' OR NAME_OF_SUBSCRIBER LIKE '%{nameOfSubscriberOp}%')
                        AND ('{fathersHusbandsNameOp}' = '' OR FATHERs_HUSBANDs_NAME LIKE '%{fathersHusbandsNameOp}%')
                        AND ('{permanentAddressOp}' = '' OR PERMANENT_ADDRESS LIKE '%{permanentAddressOp}%')
                        AND ('{LocalAddressOp}' = '' OR LOCAL_ADDRESS LIKE '%{LocalAddressOp}%')
                        AND ('{alternatePhoneNoOp}' = '' OR ALTERNATE_PHONE_NO LIKE '%{alternatePhoneNoOp}%')
                        AND ('{emailIdOp}' = '' OR E_MAILID LIKE '%{emailIdOp}%')
                        AND ('{statusOfSubscriberOp}' = '' OR STATUS_OF_SUBSCRIBER LIKE '%{statusOfSubscriberOp}%')
                        AND ('{currentStatusOfConnectionOp}' = '' OR CURRENT_STATUS_OF_CONNECTION LIKE '%{currentStatusOfConnectionOp}%')
                        ;""".format(tableName=fileName,
                                    genderOp= '' if fullGender == '' else "m" if fullGender.lower() == "male" else "f",
                                    fullGenderOp = fullGender,
                                    telephoneNumberOp=telephoneNumber,
                                    aadharNoOfCustomerOp=aadharNoOfCustomer,
                                    nameOfSubscriberOp=nameOfSubscriber,
                                    dateOfBirthFromOp=dateOfBirthFrom,
                                    dateOfBirthToOp=dateOfBirthTo,
                                    fathersHusbandsNameOp=fathersHusbandsName,
                                    permanentAddressOp=permanentAddress,
                                    alternatePhoneNoOp=alternatePhoneNo,
                                    emailIdOp=emailId,
                                    statusOfSubscriberOp=statusOfSubscriber,
                                    simActivationDateFromOp=simActivationDateFrom,
                                    simActivationDateToOp=simActivationDateTo,
                                    currentStatusOfConnectionOp=currentStatusOfConnection,
                                    LocalAddressOp=localAddress,
                                    useBirthDateOp = 1 if useBirthDate else 0,
                                    useSIMActivationDateOp = 1 if useSIMActivationDate else 0
                                    )

        return pd.read_sql(query, engine)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(readFile, MDBFiles.items())

        df = pd.concat(results)

        if(not df.empty):
            df.to_csv(outputFile, index=False, mode='w', header=True)
