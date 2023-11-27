# -*- coding: utf-8 -*-
from django.shortcuts import render
from config import settings
from barocert import NavercertService, NaverIdentity, BarocertException, \
    NaverSign, NaverMultiSign, NaverMultiSignTokens

# config/settings.py 인증정보(LinkID, SecretKey)를 이용해 설정
# NavercertService 객체 인스턴스 생성
navercertService = NavercertService(settings.LinkID, settings.SecretKey)

# 인증토큰 IP제한기능 사용여부, True-사용, False-미사용, 기본값(True)
navercertService.IPRestrictOnOff = settings.IPRestrictOnOff

# 네이버써트 API 서비스 고정 IP 사용여부, True-사용, False-미사용, 기본값(False)
navercertService.UseStaticIP = settings.UseStaticIP

# 네이버 이용자에게 본인인증을 요청합니다.
# https://developers.barocert.com/reference/naver/python/identity/api#RequestIdentity
def requestIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 본인인증 요청정보 객체
        requestObj = NaverIdentity(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = navercertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = navercertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = navercertService._encrypt('19700101'),
            
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',

            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            # appUseYN = True,

            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'ANDROID',

            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'navercert://sign'
        )

        result = navercertService.requestIdentity(clientCode, requestObj)

        return render(request, 'navercert/requestIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 본인인증 요청 후 반환받은 접수아이디로 본인인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/naver/python/identity/api#GetIdentityStatus
def getIdentityStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 본인인증 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000004'

        result = navercertService.getIdentityStatus(clientCode, receiptID)

        return render(request, 'navercert/getIdentityStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 반환받은 전자서명값(signedData)과 [1. RequestIdentity] 함수 호출에 입력한 Token의 동일 여부를 확인하여 이용자의 본인인증 검증을 완료합니다.
# 네이버 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/naver/python/identity/api#VerifyIdentity
def verifyIdentityHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 본인인증 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000003'

        result = navercertService.verifyIdentity(clientCode, receiptID)

        return render(request, 'navercert/verifyIdentity.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 네이버 이용자에게 단건(1건) 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/naver/python/sign/api-single#RequestSign
def requestSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 전자서명 요청정보 객체
        requestObj = NaverSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = navercertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = navercertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = navercertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '전자서명(단건) 요청 메시지 제목',
            # 인증요청 메시지 - 최대 500자
            reqMessage = navercertService._encrypt('전자서명(단건) 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            # 서명 원문 - 최대 2,800자 까지 입력가능
            token = navercertService._encrypt('전자서명(단건) 요청 원문'),
            
            # 서명 원문 유형
            # TEXT - 일반 텍스트, HASH - HASH 데이터
            tokenType = 'TEXT',
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            # appUseYN = True,

            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            # deviceOSType = 'ANDROID',

            # App to App 방식 이용시, 에러시 호출할 URL
            # returnURL = 'navercert://sign'
        )

        result = navercertService.requestSign(clientCode, requestObj)

        return render(request, 'navercert/requestSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명(단건) 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/naver/python/sign/api-single#GetSignStatus
def getSignStatusHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000007'

        result = navercertService.getSignStatus(clientCode, receiptID)

        return render(request, 'navercert/getSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})
    
    
# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 네이버 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/naver/python/sign/api-single#VerifySign
def verifySignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000005'

        result = navercertService.verifySign(clientCode, receiptID)

        return render(request, 'navercert/verifySign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 네이버 이용자에게 복수(최대 50건) 문서의 전자서명을 요청합니다.
# https://developers.barocert.com/reference/naver/python/sign/api-multi#RequestMultiSign
def requestMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'
        
        multiSignTokens = []
        for x in range(0,5):
            multiSignTokens.append(
                NaverMultiSignTokens(
                    # 서명 원문 유형
                    # TEXT - 일반 텍스트, HASH - HASH 데이터
                    tokenType = 'TEXT',
                    # 서명 원문 - 원문 2,800자 까지 입력가능
                    token = navercertService._encrypt("전자서명(복수) 요청 원문 " + str(x)) 
            )
        )  

        # 전자서명 요청정보 객체
        requestObj = NaverMultiSign(

            # 수신자 휴대폰번호 - 11자 (하이픈 제외)
            receiverHP = navercertService._encrypt('01012341234'),
            # 수신자 성명 - 80자
            receiverName = navercertService._encrypt('홍길동'),
            # 수신자 생년월일 - 8자 (yyyyMMdd)
            receiverBirthday = navercertService._encrypt('19700101'),
            
            # 인증요청 메시지 제목 - 최대 40자
            reqTitle = '전자서명(복수) 요청 메시지 제목',
            # 인증요청 메시지 - 최대 500자
            reqMessage = navercertService._encrypt('전자서명(복수) 요청 메시지'),
            # 고객센터 연락처 - 최대 12자
            callCenterNum = '1600-9854',
            # 인증요청 만료시간 - 최대 1,000(초)까지 입력 가능
            expireIn = 1000,
            
            # 개별문서 등록 - 최대 20 건
            tokens = multiSignTokens,
            
            # AppToApp 인증요청 여부
            # true - AppToApp 인증방식, false - Talk Message 인증방식
            #appUseYN = True,

            # 모바일장비 유형('ANDROID', 'IOS'), 대문자 입력(대소문자 구분)
            #deviceOSType = 'ANDROID',

            # App to App 방식 이용시, 에러시 호출할 URL
            #returnURL = 'navercert://sign'
        )

        result = navercertService.requestMultiSign(clientCode, requestObj)

        return render(request, 'navercert/requestMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 전자서명(복수) 요청 후 반환받은 접수아이디로 인증 진행 상태를 확인합니다.
# https://developers.barocert.com/reference/naver/python/sign/api-multi#GetMultiSignStatus
def getMultiSignStateHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000010'

        result = navercertService.getMultiSignStatus(clientCode, receiptID)

        return render(request, 'navercert/getMultiSignStatus.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})

# 완료된 전자서명을 검증하고 전자서명값(signedData)을 반환 받습니다.
# 네이버 보안정책에 따라 검증 API는 1회만 호출할 수 있습니다. 재시도시 오류가 반환됩니다.
# 전자서명 완료일시 이후에 검증 API를 호출하면 오류가 반환됩니다.
# https://developers.barocert.com/reference/naver/python/sign/api-multi#VerifyMultiSign
def verifyMultiSignHandler(request):
    try:
        # 이용기관코드, 파트너 사이트에서 확인
        clientCode = '023090000021'

        # 전자서명 요청시 반환받은 접수아이디
        receiptID = '02311010230900000210000000000009'

        result = navercertService.verifyMultiSign(clientCode, receiptID)

        return render(request, 'navercert/verifyMultiSign.html', {'result': result})
    except BarocertException as KE:
        return render(request, 'exception.html', {'code': KE.code, 'message': KE.message})