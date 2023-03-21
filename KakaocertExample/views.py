# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from kakaocert import RequestCMS, KakaocertService, RequestVerifyAuth, BarocertException, \
    RequestESign, BulkRequestESign, Tokens


# config/settings.py 인증정보(LinkID, SecretKey)를 이용해
# KakaocertService 객체 인스턴스 생성
kakaocertService = KakaocertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, 권장(True)
kakaocertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 카카오써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
kakaocertService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부 True-사용, False-미사용, 기본값(True)
kakaocertService.UseLocalTimeYN = settings.UseLocalTimeYN


# 전자서명 요청(단건)
def requestESignHandler(request):
    """
    전자서명을 요청(단건)합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # AppToApp 인증 여부
        # True-App To App 방식, False-Talk Message 방식
        appUseYN = False

        # 전자서명 요청정보 객체
        requestObj = RequestESign(

            # 요청번호 40자
            RequestID = 'kakaocert_202303130000000000000000000005',
            
            # 수신자 정보(휴대폰번호, 성명, 생년월일)와 Ci 값 중 택일
            ReceiverHP = '01087674117',
            ReceiverName = '이승환',
            ReceiverBirthday = '19930112',
            # Ci = '',

            ReqTitle = '전자서명단건테스트',
            ExpireIn = 1000,
            Token = '전자서명단건테스트데이터',
            TokenType = 'TEXT' # // TEXT, HASH
        
            # App to App 방식 이용시, 에러시 호출할 URL
            # ReturnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestESign(clientCode, requestObj, appUseYN)

        return render(request, 'resultESign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 요청(다건)
def bulkReqeustESignHandler(request):
    """
    전자서명을 요청(다건)합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # AppToApp 인증 여부
        # True-App To App 방식, False-Talk Message 방식
        appUseYN = False

        # 전자서명 요청정보 객체
        requestObj = BulkRequestESign(

            # 요청번호 40자
            RequestID = 'kakaocert_202303130000000000000000000005',
            
            # 수신자 정보(휴대폰번호, 성명, 생년월일)와 Ci 값 중 택일
            ReceiverHP = '01087674117',
            ReceiverName = '이승환',
            ReceiverBirthday = '19930112',
            # Ci = '',

            ReqTitle = '전자서명다건테스트',
            ExpireIn = 1000,
            TokenType = 'TEXT' # // TEXT, HASH
        
            # App to App 방식 이용시, 에러시 호출할 URL
            # ReturnURL = 'https://kakao.barocert.com'
        )

        requestObj.Tokens = []

        requestObj.Tokens.append(
            Tokens(
                reqTitle = '전자서명다건문서테스트1',
                token = '전자서명다건테스트데이터1'
            )
        )
        requestObj.Tokens.append(
            Tokens(
                reqTitle = '전자서명다건문서테스트2',
                token = '전자서명다건테스트데이터2'
            )
        )

        result = kakaocertService.bulkRequestESign(clientCode, requestObj, appUseYN)

        return render(request, 'bulkRequestESign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 상태확인(단건)
def getESignStateHandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명 상태를 확인(단건)합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '0230309201738000000000000000000000000001'

        result = kakaocertService.getESignState(clientCode, receiptId)

        return render(request, 'getESignState.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 상태확인(다건)
def getBulkESignStateHandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명 상태를 확인(다건)합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '0230309201738000000000000000000000000001'

        result = kakaocertService.getBulkESignState(clientCode, receiptId)

        return render(request, 'getBulkESignState.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 검증(단건)
def verifyESignHandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명을 검증(단건)합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '0230310143306000000000000000000000000001'

        result = kakaocertService.verifyESign(clientCode, receiptId)

        return render(request, 'verifyESign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 검증(다건)
def bulkVerifyESignHandler(request):
    """
    전자서명 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '0230310143306000000000000000000000000001'

        result = kakaocertService.bulkVerifyESign(clientCode, receiptId)

        return render(request, 'bulkVerifyESign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 요청
def requestVerifyAuthHandler(request):
    """
    본인인증 전자서명을 요청합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청정보 객체
        requestObj = RequestVerifyAuth(

            # 요청번호 40자
            RequestID = 'kakaocert_202303130000000000000000000001',

            # 수신자 정보(휴대폰번호, 성명, 생년월일)와 Ci 값 중 택일
            ReceiverHP = '01087674117',
            ReceiverName = '이승환',
            ReceiverBirthday = '19930112',
            # Ci = '',

            ReqTitle = '인증요청 메시지 제목란',
            ExpireIn = 1000,
            Token = '본인인증요청토큰'

            # App to App 방식 이용시, 에러시 호출할 URL
            # ReturnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestVerifyAuth(clientCode, requestObj)

        return render(request, 'requestVerifyAuth.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 상태확인
def getVerifyAuthStateHandler(request):
    """
    본인인증 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '022050912192100001'

        result = kakaocertService.getVerifyAuthState(clientCode, receiptId)

        return render(request, 'getVerifyAuthState.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 검증
def verifyAuthHandler(request):
    """
    본인인증 요청시 반환된 접수아이디를 통해 본인인증 서명을 검증합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '022050912192100001'

        result = kakaocertService.verifyAuth(clientCode, receiptId)

        return render(request, 'verifyAuth.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 출금동의 요청
def requestCMSHandler(request):
    """
    자동이체 출금동의 전자서명을 요청합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # AppToApp 인증 여부
        # True-App To App 방식, False-Talk Message 방식
        appUseYN = False

        # 자동이체 출금동의 요청정보 객체
        requestObj = RequestCMS(
            # 요청번호 40자
            RequestID = 'kakaocert_202303130000000000000000000001',

            # 수신자 정보(휴대폰번호, 성명, 생년월일)와 Ci 값 중 택일
            ReceiverHP = '01087674117',
            ReceiverName = '이승환',
            ReceiverBirthday = '19930112',
            # Ci = '',

            ReqTitle = '인증요청 메시지 제목란',
            ExpireIn = 1000,

            RequestCorp = '청구 기관명란',
            BankName = '출금은행명란',
            BankAccountNum = '9-4324-5117-58',
            BankAccountName = '예금주명 입력란',
            BankAccountBirthday = '19930112',
            BankServiceType = 'CMS', # CMS, FIRM, GIRO

            # App to App 방식 이용시, 에러시 호출할 URL
            # ReturnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestCMS(clientCode, requestObj, appUseYN)

        return render(request, 'requestCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 출금동의 상태확인
def getCMSStateHandler(request):
    """
    자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '0230309201738000000000000000000000000001'

        result = kakaocertService.getCMSState(clientCode, receiptId)

        return render(request, 'getCMSState.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 출금동의 검증
def verifyCMSHandler(request):
    """
    자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
    - 
    """
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '020040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '0230309201738000000000000000000000000001'

        result = kakaocertService.verifyCMS(clientCode, receiptId)

        return render(request, 'verifyCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
