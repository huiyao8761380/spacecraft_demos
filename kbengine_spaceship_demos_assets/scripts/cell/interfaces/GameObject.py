# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import d_entities
import d_avatar_inittab
import SCDefine

class GameObject:

    def __init__(self):
        pass

    def initEntity(self):
        """
        virtual method.
        """
        pass

    def isPlayer(self):
        """
        virtual method.
        """
        return False

    def isSupplyBox(self):
        """
        virtual method.
        """
        return False

    def isMine(self):
        """
        virtual method.
        """
        return False

    def isWeapon(self):
        """
        virtual method.
        """
        return False

    def getDatas(self):
        if self.isPlayer():
            return d_avatar_inittab.datas[self.uid]

        return d_entities.datas[self.uid]

    def getLvPops(self):
        if self.isPlayer():
            return d_avatar_inittab.upgrade_props[self.level]
        return None

    def getUpperExp(self):
        if self.isPlayer():
            return {k:v['exp'] for k,v in d_avatar_inittab.upgrade_props.items() if k >= self.level}
        return None


    def getScriptNmae(self):
        return self.__class__.__name__


    def getCurrSpaceBase(self):
        """
        获得当前space的entity baseEntityCall
        """
        DEBUG_MSG('GameObject::getCurrSpaceBase: spaceID = %i' % self.spaceID)
        return KBEngine.globalData.get("Space_%i" % self.spaceID)

    def getCurrSpace(self):
        """
        获得当前space的entity
        """
        spaceBase = self.getCurrSpaceBase()
        if spaceBase is None:
            return spaceBase

        return KBEngine.entities.get(spaceBase.id, None)

    def getSpaces(self):
        """
        获取场景管理器
        """
        return KBEngine.globalData["Spaces"]

    def startDestroyTimer(self):
        """
        virtual method.

        启动销毁entitytimer
        """
        self.addTimer(5, 0, SCDefine.TIMER_TYPE_DESTROY)
        DEBUG_MSG("%s::startDestroyTimer: %i running." % (self.getScriptName(), self.id))

    def onTimer(self,tid,userArg):
        """
        virtual method.

        启动销毁entitytimer
        """
        if SCDefine.TIMER_TYPE_DESTROY == userArg:
            self.onDestroyEntityTimer()

    def getScriptName(self):
        return self.__class__.__name__

    def onWitnessed(self, isWitnessed):
        """
        KBEngine method.
        此实体是否被观察者(player)观察到, 此接口主要是提供给服务器做一些性能方面的优化工作，
        在通常情况下，一些entity不被任何客户端所观察到的时候， 他们不需要做任何工作， 利用此接口
        可以在适当的时候激活或者停止这个entity的任意行为。
        @param isWitnessed	: 为false时， entity脱离了任何观察者的观察
        """
        DEBUG_MSG("%s::onWitnessed: %i isWitnessed=%i." % (self.getScriptName(), self.id, isWitnessed))

    def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
        """
        KBEngine method.
        引擎回调进入陷阱触发
        """
        if entityEntering.getScriptName() == "Avatar":
            DEBUG_MSG("%s::onEnterTrap: %i entityEntering=%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
                            (self.getScriptName(), self.id, entityEntering.id, range_xz, range_y, controllerID, userarg))

    def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
        """
        KBEngine method.
        引擎回调离开陷阱触发
        """
        if entityLeaving.getScriptName() == "Avatar":
            DEBUG_MSG("%s::onLeaveTrap: %i entityLeaving=%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
                            (self.getScriptName(), self.id, entityLeaving.id, range_xz, range_y, controllerID, userarg))


    def onRestore(self):
        """
        KBEngine method.
        entity的cell部分实体被恢复成功
        """
        DEBUG_MSG("%s::onRestore: %s" % (self.getScriptName(), self.base))

    def onDestroyEntityTimer(self):
        """
        entity的延时销毁timer
        """
        DEBUG_MSG("%s::onDestroyEntityTimer: %i destroy." % (self.getScriptName(), self.id))
        self.destroy()