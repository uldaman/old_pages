author: Martin
date: 2015-06-13 06:27
title: [CEGUI]. 5、解决电脑休眠引起的黑屏问题

在做游戏的时候发现个问题, 就是当电脑休眠再唤醒后, 游戏界面会失去响应.

查阅资料发现, 电脑休眠时 D3D 会丢失设备, 当唤醒后, D3D 会调用 IDirect3DDevice9::Reset() 解决这个问题, 原始的 HOOK 后的 IDirect3DDevice9::Reset() 是下面这样:

```c++
HRESULT APIENTRY hkIDirect3DDevice9::Reset(D3DPRESENT_PARAMETERS *pPresentationParameters) {
    m_pManager->PreReset();

    HRESULT hRet = m_pD3Ddev->Reset(pPresentationParameters);

    if (SUCCEEDED(hRet)) {
        m_PresentParam = *pPresentationParameters;
        m_pManager->PostReset();
    }

    return hRet;
}
```

进入游戏初始化 CEGUI 界面, 然后休眠电脑, 再唤醒, 发现 hRet 返回 0x8876086C, 即 Reset 失败;
如果不初始化 CEGUI 界面, 直接休眠电脑, 再唤醒则是正常的, 于是查阅 CEGUI 源代码, 发现了问题所在, 如果我们使用了 CEGUI, 那么就需要重写 Rest 方法:

```c++
HRESULT APIENTRY hkIDirect3DDevice9::Reset(D3DPRESENT_PARAMETERS *pPresentationParameters) {
    CEGUI::Direct3D9Renderer* d3d_renderer = nullptr;
    if (theApp.m_bInit) {
        CEGUI::System* cegui_system = CEGUI::System::getSingletonPtr();
        d3d_renderer = static_cast<CEGUI::Direct3D9Renderer*>(cegui_system->getRenderer());
    }

    if (theApp.m_bInit) {
        d3d_renderer->preD3DReset();
    } else {
        m_pManager->PreReset();
    }

    HRESULT hRet = m_pD3Ddev->Reset(pPresentationParameters);

    if (SUCCEEDED(hRet)) {
        m_PresentParam = *pPresentationParameters;

        if (theApp.m_bInit) {
            d3d_renderer->postD3DReset();
        } else {
            m_pManager->PostReset();
        }
    }

    return hRet;
}
```
