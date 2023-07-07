# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from barocert import KakaoCMS, KakaocertService, KakaoIdentity, BarocertException, \
    KakaoSign, KakaoMultiSign, KakaoMultiSignTokens


# config/settings.py 인증정보(LinkID, SecretKey)를 이용해
# KakaocertService 객체 인스턴스 생성
kakaocertService = KakaocertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, 권장(True)
kakaocertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 카카오써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
kakaocertService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부 True-사용, False-미사용, 기본값(True)
kakaocertService.UseLocalTimeYN = settings.UseLocalTimeYN

# 카카오톡 사용자에게 본인인증 전자서명을 요청합니다.
# https://developers.barocert.com/reference/kakao/java/identity/api#RequestIdentity
def requestIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 본인인증 요청정보 객체
        requestObj = KakaoIdentity(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = kakaocertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = kakaocertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = kakaocertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '인증요청 메시지 제목란',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 40자 까지 입력가능
            token = kakaocertService._encrypt('본인인증요청토큰'),
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            appUseYN = False,

            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestIdentity(clientCode, requestObj)

        return render(request, 'requestIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
# https://developers.barocert.com/reference/kakao/java/identity/api#GetIdentityStatus
def getIdentityStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000012'

        result = kakaocertService.getIdentityStatus(clientCode, receiptId)

        return render(request, 'getIdentityStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 요청시 반환된 접수아이디를 통해 본인인증 서명을 검증합니다. 
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다.
# https://developers.barocert.com/reference/kakao/java/identity/api#VerifyIdentity
def verifyIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000012'

        result = kakaocertService.verifyIdentity(clientCode, receiptId)

        return render(request, 'verifyIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 사용자에게 전자서명을 요청합니다.(단건)
# https://developers.barocert.com/reference/kakao/java/sign/api-single#RequestSign
def requestSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 전자서명 요청정보 객체
        requestObj = KakaoSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = kakaocertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = kakaocertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = kakaocertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '인증요청 메시지 제목란',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 2,800자 까지 입력가능
            token = kakaocertService._encrypt('본인인증요청토큰'),
            
            # 서명 원문 유형
            # TEXT - 일반 텍스트, HASH - HASH 데이터
            tokenType = 'TEXT',
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            appUseYN = False,
        
            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestSign(clientCode, requestObj)

        return render(request, 'requestSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 요청시 반환된 접수아이디를 통해 서명을 검증합니다. (단건)
# https://developers.barocert.com/reference/kakao/java/sign/api-single#GetSignStatus
def getSignStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000016'

        result = kakaocertService.getSignStatus(clientCode, receiptId)

        return render(request, 'getSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
    
    
# 전자서명 요청시 반환된 접수아이디를 통해 서명을 검증합니다. (단건)
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다
# https://developers.barocert.com/reference/kakao/java/sign/api-single#VerifySign
def verifySignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000016'

        result = kakaocertService.verifySign(clientCode, receiptId)

        return render(request, 'verifySign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 사용자에게 전자서명을 요청합니다.(복수)
# https://developers.barocert.com/reference/kakao/java/sign/api-multi#RequestMultiSign
def requestMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'
        
        multiSignTokens = []
        for x in range(0,5):
            multiSignTokens.append(
                KakaoMultiSignTokens(
                    # 인증요청 메시지 제목 - 최대 40자
                    reqTitle = "전자서명복수테스트",
                    # 서명 원문 - 원문 2,800자 까지 입력가능
                    token = kakaocertService._encrypt("전자서명복수테스트데이터" + str(x)) 
            )
        )  

        # 전자서명 요청정보 객체
        requestObj = KakaoMultiSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = kakaocertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = kakaocertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = kakaocertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '인증요청 메시지 제목란',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # 개별문서 등록 - 최대 20 건
            tokens = multiSignTokens,
            
            # 서명 원문 유형
            # TEXT - 일반 텍스트, HASH - HASH 데이터
            tokenType = 'TEXT',
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            appUseYN = False,
        
            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestMultiSign(clientCode, requestObj)

        return render(request, 'requestMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다. (복수)
# https://developers.barocert.com/reference/kakao/java/sign/api-multi#GetMultiSignStatus
def getMultiSignStateHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000022'

        result = kakaocertService.getMultiSignStatus(clientCode, receiptId)

        return render(request, 'getMultiSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명 요청시 반환된 접수아이디를 통해 서명을 검증합니다. (복수)
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다.
# https://developers.barocert.com/reference/kakao/java/sign/api-multi#VerifyMultiSign
def verifyMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000022'

        result = kakaocertService.verifyMultiSign(clientCode, receiptId)

        return render(request, 'verifyMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 사용자에게 자동이체 출금동의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/kakao/java/cms/api#RequestCMS
def requestCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 자동이체 출금동의 요청정보 객체
        requestObj = KakaoCMS(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = kakaocertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = kakaocertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = kakaocertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '인증요청 메시지 제목란',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # 청구기관명 - 최대 100자
            requestCorp = kakaocertService._encrypt('청구 기관명란'),
            # 출금은행명 - 최대 100자
            bankName = kakaocertService._encrypt('출금은행명란'),
            # 출금계좌번호 - 최대 32자
            bankAccountNum = kakaocertService._encrypt('9-4324-5117-58'),
            # 출금계좌 예금주명 - 최대 100자
            bankAccountName = kakaocertService._encrypt('예금주명 입력란'),
            # 출금계좌 예금주 생년월일 - 8자
            bankAccountBirthday = kakaocertService._encrypt('19700101'),
            # 출금유형
            # CMS - 출금동의용, FIRM - 펌뱅킹, GIRO - 지로용
            bankServiceType = kakaocertService._encrypt('CMS'),
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            appUseYN = False,

            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'https://kakao.barocert.com'
        )

        result = kakaocertService.requestCMS(clientCode, requestObj)

        return render(request, 'requestCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명 상태를 확인합니다.
#https://developers.barocert.com/reference/kakao/java/cms/api#GetCMSStatus
def getCMSStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000023'

        result = kakaocertService.getCMSStatus(clientCode, receiptId)

        return render(request, 'getCMSStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 자동이체 출금동의 요청시 반환된 접수아이디를 통해 서명을 검증합니다.
# 검증하기 API는 완료된 전자서명 요청당 1회만 요청 가능하며, 사용자가 서명을 완료후 유효시간(10분)이내에만 요청가능 합니다.
# https://developers.barocert.com/reference/kakao/java/cms/api#VerifyCMS
def verifyCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023030000004'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230300000040000000000023'

        result = kakaocertService.verifyCMS(clientCode, receiptId)

        return render(request, 'verifyCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
