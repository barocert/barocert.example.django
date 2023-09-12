# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from barocert import PassCMS, PassIdentity, PassLogin, PassSign, \
                    PassCMSVerify, PassIdentityVerify, PassLoginVerify, PassSignVerify, \
                    PasscertService,  BarocertException

# config/settings.py 인증정보(LinkID, SecretKey)를 이용해
# PasscertService 객체 인스턴스 생성
passcertService = passcertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, True-사용, False-미사용, 기본값(True)
passcertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 패스써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
passcertService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, True-사용, False-미사용, 기본값(True)
passcertService.UseLocalTimeYN = settings.UseLocalTimeYN

# 패스 이용자에게 본인인증을 요청합니다.
# https://developers.barocert.com/reference/pass/dotnetcore/identity/api#RequestIdentity
def requestIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 본인인증 요청정보 객체
        requestObj = PassIdentity(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01067668440'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('정우석'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19900911'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '인증요청 메시지 제목란',
            # 인증요청 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('인증요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 40자 까지 입력가능
            token = passcertService._encrypt('본인인증요청토큰'),
            
            # 사용자 동의 필요 여부
            userAgreementYN = True;
            # 사용자 정보 포함 여부
            receiverInfoYN = True;

            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Push 인증방식
            appUseYN = False;
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT';
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS';
        )

        result = passcertService.requestIdentity(clientCode, requestObj)

        return render(request, 'passcert/requestIdentity.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 본인인증 요청 후 반환받은 접수아이디로 본인인증 진행 상태를 확인합니다.
# 상태확인 함수는 본인인증 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 본인인증 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/dotnetcore/identity/api#GetIdentityStatus
def getIdentityStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000012'

        result = passcertService.getIdentityStatus(clientCode, receiptId)

        return render(request, 'passcert/getIdentityStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})


# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 반환받은 전자서명값(signedData)과 [1. RequestIdentity] 함수 호출에 입력한 Token의 동일 여부를 확인하여 이용자의 본인인증 검증을 완료합니다.
# 검증 함수는 본인인증 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 본인인증 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/dotnetcore/identity/api#VerifyIdentity
def verifyIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000012'

        # 검증 요청 정보 객체
        verifyObj = PassIdentityVerify(
            receiverHP = passcertService._encrypt('01067668440'),
            receiverName = passcertService._encrypt('정우석'),
        )

        result = passcertService.verifyIdentity(clientCode, receiptId, verifyObj)

        return render(request, 'passcert/verifyIdentity.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 패스 이용자에게 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/pass/dotnetcore/sign/api#RequestSign
def requestSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청정보 객체
        requestObj = PassSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01067668440'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('정우석'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19900911'),
            
            # 전자서명 메시지 제목 - 최대 40자
            reqTitle = '전자서명 메시지 제목란',
            # 전자서명 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('전자서명 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 전자서명 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 2,800자 까지 입력가능
            token = passcertService._encrypt('전자서명요청토큰'),
            
            # 서명 원문 유형
            # 'TEXT' - 일반 텍스트, 'HASH' - HASH 데이터, 'URL' - URL 데이터
            # 원본데이터(originalTypeCode, originalURL, originalFormatCode) 입력시 'TEXT'사용 불가
            tokenType = 'URL',
            
            # 사용자 동의 필요 여부
            userAgreementYN = True;
            # 사용자 정보 포함 여부
            receiverInfoYN = True;

            # 원본유형코드
            # 'AG' - 동의서, 'AP' - 신청서, 'CT' - 계약서, 'GD' - 안내서, 'NT' - 통지서, 'TR' - 약관
            originalTypeCode = 'TR',
            # 원본조회URL
            originalURL = 'https://www.passcert.co.kr',
            # 원본형태코드
            # ('TEXT', 'HTML', 'DOWNLOAD_IMAGE', 'DOWNLOAD_DOCUMENT')
            originalFormatCode = 'HTML',

            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Push 인증방식
            appUseYN = False;
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT';
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS';
        )

        result = passcertService.requestSign(clientCode, requestObj)

        return render(request, 'passcert/requestSign.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 전자서명 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# 상태확인 함수는 전자서명 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 전자서명 요청 함수를 호출한 당일 23시 59분 59초 이후 상태확인 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/dotnetcore/sign/api#GetSignStatus
def getSignStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000016'

        result = passcertService.getSignStatus(clientCode, receiptId)

        return render(request, 'passcert/getSignStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})
    
# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 검증 함수는 전자서명 요청 함수를 호출한 당일 23시 59분 59초까지만 호출 가능합니다.
# 전자서명 요청 함수를 호출한 당일 23시 59분 59초 이후 검증 함수를 호출할 경우 오류가 반환됩니다.
# https://developers.barocert.com/reference/pass/dotnetcore/sign/api#VerifySign
def verifySignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000016'

        # 검증 요청 정보 객체
        verifyObj = PassIdentityVerify(
            receiverHP = passcertService._encrypt('01067668440'),
            receiverName = passcertService._encrypt('정우석'),
        )

        result = passcertService.verifySign(clientCode, receiptId, verifyObj)

        return render(request, 'passcert/verifySign.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 패스 이용자에게 자동이체 출금동의를 요청합니다.
# https://developers.barocert.com/reference/pass/dotnetcore/cms/api#RequestCMS
def requestCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 자동이체 출금동의 요청정보 객체
        requestObj = PassCMS(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = passcertService._encrypt('01067668440'),
            # 수신자 성명 - 80자
            receiverName = passcertService._encrypt('정우석'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = passcertService._encrypt('19900911'),
            
            # 요청 메시지 제목 - 최대 40자
            reqTitle = '출금동의 메시지 제목란',
            # 요청 메시지 - 최대 500자
            reqMessage = passcertService._encrypt('출금동의 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # 사용자 동의 필요 여부
            userAgreementYN = True;
            # 사용자 정보 포함 여부
            receiverInfoYN = True;

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
            # true - AppToApp 인증방식, false - Push 인증방식
            appUseYN = False;
            # ApptoApp 인증방식에서 사용
            # 통신사 유형('SKT', 'KT', 'LGU'), 대문자 입력(대소문자 구분)
            # telcoType = 'SKT';
            # ApptoApp 인증방식에서 사용
            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'IOS';
        )

        result = passcertService.requestCMS(clientCode, requestObj)

        return render(request, 'passcert/requestCMS.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
def getCMSStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000023'

        result = passcertService.getCMSStatus(clientCode, receiptId)

        return render(request, 'passcert/getCMSStatus.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다.
def verifyCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000023'

        result = passcertService.verifyCMS(clientCode, receiptId)

        return render(request, 'passcert/verifyCMS.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})

# 간편로그인 요청시 반환된 트랜잭션 아이디를 통해 서명을 검증합니다.
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다.
def verifyLoginHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 간편로그인 요청시 반환받은 트랜잭션 아이디
        txId = '02304200230400000010000000000023'

        result = passcertService.verifyLogin(clientCode, receiptId)

        return render(request, 'passcert/verifyLogin.html', {'result': result})
    except BarocertException as PE:
        return render(request, 'exception.html', {'code': PE.code, 'message': PE.message})