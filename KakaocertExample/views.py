# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from barocert import KakaoCMS, KakaocertService, KakaoIdentity, BarocertException, \
    KakaoSign, KakaoMultiSign, KakaoMultiSignTokens

# config/settings.py 인증정보(LinkID, SecretKey)를 이용해 설정
# KakaocertService 객체 인스턴스 생성
kakaocertService = KakaocertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, True-사용, False-미사용, 기본값(True)
kakaocertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 카카오써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
kakaocertService.UseStaticIP = settings.UseStaticIP

# 로컬시스템 시간 사용여부, True-사용, False-미사용, 기본값(True)
kakaocertService.UseLocalTimeYN = settings.UseLocalTimeYN

# 카카오톡 이용자에게 본인인증을 요청합니다.
# https://developers.barocert.com/reference/kakao/python/identity/api#RequestIdentity
def requestIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

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

        return render(request, 'kakaocert/requestIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 요청 후 반환받은 접수아이디로 본인인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/kakao/python/identity/api#GetIdentityStatus
def getIdentityStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000012'

        result = kakaocertService.getIdentityStatus(clientCode, receiptId)

        return render(request, 'kakaocert/getIdentityStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 반환받은 전자서명값(signedData)과 [1. RequestIdentity] 함수 호출에 입력한 Token의 동일 여부를 확인하여 이용자의 본인인증 검증을 완료합니다.
# 카카오 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시로부터 10분 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/kakao/python/identity/api#VerifyIdentity
def verifyIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 본인인증 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000012'

        result = kakaocertService.verifyIdentity(clientCode, receiptId)

        return render(request, 'kakaocert/verifyIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 이용자에게 단건(1건) 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-single#RequestSign
def requestSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

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

        return render(request, 'kakaocert/requestSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명(단건) 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-single#GetSignStatus
def getSignStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000016'

        result = kakaocertService.getSignStatus(clientCode, receiptId)

        return render(request, 'kakaocert/getSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
    
    
# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 카카오 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시로부터 10분 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-single#VerifySign
def verifySignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000016'

        result = kakaocertService.verifySign(clientCode, receiptId)

        return render(request, 'kakaocert/verifySign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 이용자에게 복수(최대 20건) 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-multi#RequestMultiSign
def requestMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'
        
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

        return render(request, 'kakaocert/requestMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명(복수) 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-multi#GetMultiSignStatus
def getMultiSignStateHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000022'

        result = kakaocertService.getMultiSignStatus(clientCode, receiptId)

        return render(request, 'kakaocert/getMultiSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 카카오 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시로부터 10분 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/kakao/python/sign/api-multi#VerifyMultiSign
def verifyMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 전자서명 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000022'

        result = kakaocertService.verifyMultiSign(clientCode, receiptId)

        return render(request, 'kakaocert/verifyMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 카카오톡 이용자에게 자동이체 출금동의를 요청합니다.
# https://developers.barocert.com/reference/kakao/python/cms/api#RequestCMS
def requestCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

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

        return render(request, 'kakaocert/requestCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 자동이체 출금동의 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/kakao/python/cms/api#GetCMSStatus
def getCMSStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000023'

        result = kakaocertService.getCMSStatus(clientCode, receiptId)

        return render(request, 'kakaocert/getCMSStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 카카오 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시로부터 10분 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/kakao/python/cms/api#VerifyCMS
def verifyCMSHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 자동이체 출금동의 요청시 반환받은 접수아이디
        receiptId = '02304200230400000010000000000023'

        result = kakaocertService.verifyCMS(clientCode, receiptId)

        return render(request, 'kakaocert/verifyCMS.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명 데이터 전문(signedData)을 반환 받습니다.
# 카카오 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시로부터 10분 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/kakao/dotnetcore/login/api#VerifyLogin
def verifyLoginHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023040000001'

        # 간편로그인 요청시 반환받은 트랜잭션 아이디
        txId = '0199a61d5b-929e-4ade-97fc-554a48cf954d'

        result = kakaocertService.verifyLogin(clientCode, txId)

        return render(request, 'kakaocert/verifyLogin.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})