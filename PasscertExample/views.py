# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from barocert import PassCMS, PassIdentity, PassLogin, PassSign, \
                    PassCMSVerify, PassIdentityVerify, PassLoginVerify, PassSignVerify, \
                    PasscertService,  BarocertException

# config/settings.py 인증정보(LinkID, SecretKey)를 이용해 설정
# PasscertService 객체 인스턴스 생성
passcertService = PasscertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP 검증 설정, true-사용, false-미사용, (기본값:true)
passcertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 통신 IP 고정, true-사용, false-미사용, (기본값:false)
passcertService.UseStaticIP = settings.UseStaticIP

# 패스 이용자에게 본인인증을 요청합니다.
# https://developers.barocert.com/reference/pass/python/identity/api#RequestIdentity
def requestIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        file = open("./barocert.pdf", 'rb')
        target = file.read()
        file.close()

        # 본인인증 요청정보 객체
        requestObj = PassIdentity(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '본인인증 요청 메시지 제목',
            # 인증요청 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('본인인증 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 40자 까지 입력가능
            token = passcertService._encrypt('본인인증 요청 원문'),
            
            # 사용자 동의 필요 여부
            userAgreementYN = True,
            # 사용자 정보 포함 여부
            receiverInfoYN = True,

            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - 푸시(push) 인증방식
            appUseYN = False,
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT',
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS',
        )

        result = passcertService.requestIdentity(clientCode, requestObj)

        return render(request, 'passcert/requestIdentity.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 본인인증 요청 후 반환받은 접수아이디로 본인인증 진행 상태를 확인합니다.
# 상태확인 함수는 본인인증 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 본인인증 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/python/identity/api#GetIdentityStatus
def getIdentityStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 본인인증 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000012'

        result = passcertService.getIdentityStatus(clientCode, receiptID)

        return render(request, 'passcert/getIdentityStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 반환받은 전자서명값(signedData)과 [1. RequestIdentity] 함수 호출에 입력한 Token의 동일 여부를 확인하여 이용자의 본인인증 검증을 완료합니다.
# 검증 함수는 본인인증 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 본인인증 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/python/identity/api#VerifyIdentity
def verifyIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 본인인증 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000012'

        # 검증 요청 정보 객체
        verifyObj = PassIdentityVerify(
            receiverHP = passcertService._encrypt('01012341234'),
            receiverName = passcertService._encrypt('홍길동'),
        )

        result = passcertService.verifyIdentity(clientCode, receiptID, verifyObj)

        return render(request, 'passcert/verifyIdentity.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 패스 이용자에게 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/pass/python/sign/api#RequestSign
def requestSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'
    
        # file = open("./barocert.pdf", 'rb')
        # target = file.read()
        # file.close()

        # 전자서명 요청정보 객체
        requestObj = PassSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19700101'),
            
            # 전자서명 메시지 제목 - 최대 40자
            reqTitle = '전자서명 요청 메시지 제목',
            # 전자서명 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('전자서명 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 전자서명 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 유형
            # 'TEXT' - 일반 텍스트, 'HASH' - HASH 데이터, 'URL' - URL 데이터
            # 원본데이터(originalTypeCode, originalURL, originalFormatCode) 입력시 'TEXT'사용 불가
            tokenType = 'URL',
            # 서명 원문 - 최대 2,800자 까지 입력가능
            token = passcertService._encrypt('전자서명 요청 원문'),
            # 서명 원문 유형
            # tokenType = 'PDF',
            # 서명 원문 유형이 PDF인 경우, 원문은 SHA-256, Base64 URL Safe No Padding을 사용
            # token = passcertService._encrypt(passcertService._sha256_base64url_file(target)),
            
            # 사용자 동의 필요 여부
            userAgreementYN = True,
            # 사용자 정보 포함 여부
            receiverInfoYN = True,

            # 원본유형코드
            # 'AG' - 동의서, 'AP' - 신청서, 'CT' - 계약서, 'GD' - 안내서, 'NT' - 통지서, 'TR' - 약관
            originalTypeCode = 'TR',
            # 원본조회URL
            originalURL = 'https://www.passcert.co.kr',
            # 원본형태코드
            # ('TEXT', 'HTML', 'DOWNLOAD_IMAGE', 'DOWNLOAD_DOCUMENT')
            originalFormatCode = 'HTML',

            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - 푸시(push) 인증방식
            appUseYN = False,
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT',
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS',
        )

        result = passcertService.requestSign(clientCode, requestObj)

        return render(request, 'passcert/requestSign.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 전자서명 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# 상태확인 함수는 전자서명 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 전자서명 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/python/sign/api#GetSignStatus
def getSignStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000016'

        result = passcertService.getSignStatus(clientCode, receiptID)

        return render(request, 'passcert/getSignStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
    
# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 검증 함수는 전자서명 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 전자서명 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/python/sign/api#VerifySign
def verifySignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000016'

        # 검증 요청 정보 객체
        verifyObj = PassSignVerify(
            receiverHP = passcertService._encrypt('01012341234'),
            receiverName = passcertService._encrypt('홍길동'),
        )

        result = passcertService.verifySign(clientCode, receiptID, verifyObj)

        return render(request, 'passcert/verifySign.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 패스 이용자에게 자동이체 출금동의를 요청합니다.
# https://developers.barocert.com/reference/pass/python/cms/api#RequestCMS
def requestCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 자동이체 출금동의 요청정보 객체
        requestObj = PassCMS(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19700101'),
            
            # 요청 메시지 제목 - 최대 40자
            reqTitle = '출금동의 요청 메시지 제목',
            # 요청 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('출금동의 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # 사용자 동의 필요 여부
            userAgreementYN = True,
            # 사용자 정보 포함 여부
            receiverInfoYN = True,

            # 출금은행명 - 최대 100자
            bankName = passcertService._encrypt('국민은행'),
            # 출금계좌번호 - 최대 32자
            bankAccountNum = passcertService._encrypt('9-****-5117-58'),
            # 출금계좌 예금주명 - 최대 100자
            bankAccountName = passcertService._encrypt('홍길동'),
            # 출금계좌 예금주 생년월일 - 8자
            bankAccountBirthday = passcertService._encrypt('19700101'),
            # 출금유형
            # CMS - 출금동의, OPEN_BANK - 오픈뱅킹
            bankServiceType = passcertService._encrypt('CMS'),
            # 출금액
            bankWithdraw = passcertService._encrypt('1,000,000원'),
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - 푸시(push) 인증방식
            appUseYN = False,
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT',
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS',
        )

        result = passcertService.requestCMS(clientCode, requestObj)

        return render(request, 'passcert/requestCMS.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 자동이체 출금동의 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# 상태확인 함수는 자동이체 출금동의 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 자동이체 출금동의 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# http://developers.barocert.com/reference/pass/python/cms/api#GetCMSStatus
def getCMSStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000023'

        result = passcertService.getCMSStatus(clientCode, receiptID)

        return render(request, 'passcert/getCMSStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 검증 함수는 자동이체 출금동의 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 자동이체 출금동의 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# http://developers.barocert.com/reference/pass/python/cms/api#VerifyCMS
def verifyCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000023'

        # 검증 요청 정보 객체
        verifyObj = PassCMSVerify(
            receiverHP = passcertService._encrypt('01012341234'),
            receiverName = passcertService._encrypt('홍길동'),
        )

        result = passcertService.verifyCMS(clientCode, receiptID, verifyObj)

        return render(request, 'passcert/verifyCMS.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 패스 이용자에게 간편로그인을 요청합니다.
# https://developers.barocert.com/reference/pass/python/login/api#RequestLogin
def requestLoginHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 간편로그인 요청정보 객체
        requestObj = PassLogin(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19700101'),
            
            # 요청 메시지 제목 - 최대 40자
            reqTitle = '간편로그인 요청 메시지 제목',
            # 요청 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('간편로그인 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 40자 까지 입력가능
            token = passcertService._encrypt('간편로그인 요청 원문'),
            
            # 사용자 동의 필요 여부
            userAgreementYN = True,
            # 사용자 정보 포함 여부
            receiverInfoYN = True,

            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - 푸시(push) 인증방식
            appUseYN = False,
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT',
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS',
        )

        result = passcertService.requestLogin(clientCode, requestObj)

        return render(request, 'passcert/requestLogin.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 간편로그인 요청 후 반환받은 접수아이디로 진행 상태를 확인합니다.
# 상태확인 함수는 간편로그인 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 간편로그인 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# http://developers.barocert.com/reference/pass/python/login/api#GetLoginStatus
def getLoginStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 간편로그인 요청시 반환받은 접수아이디
        receiptID = '02304200230700000140000000000023'

        result = passcertService.getLoginStatus(clientCode, receiptID)

        return render(request, 'passcert/getLoginStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 검증 함수는 간편로그인 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 간편로그인 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# http://developers.barocert.com/reference/pass/python/login/api#VerifyLogin
def verifyLoginHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023070000014'

        # 간편로그인 요청시 반환받은 트랜잭션 아이디
        receiptID = '02304200230700000140000000000023'

        # 검증 요청 정보 객체
        verifyObj = PassLoginVerify(
            receiverHP = passcertService._encrypt('01012341234'),
            receiverName = passcertService._encrypt('홍길동'),
        )

        result = passcertService.verifyLogin(clientCode, receiptID, verifyObj)

        return render(request, 'passcert/verifyLogin.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})