<template>
  <section>
    <a-breadcrumb style="margin-bottom: 30px">
      <a-breadcrumb-item href="">
        <a-icon type="home" />
      </a-breadcrumb-item>
      <a-breadcrumb-item href="">
        <span>{{title}}</span>
      </a-breadcrumb-item>
    </a-breadcrumb>
    <a-card id="profile" hoverable title="个人信息" :style="{margin:'auto',minWidth:'230px',width: '80%', minHeight:'200px'}">
      <a-row type="flex" justify="start" style="margin-bottom: 20px">
        <a-col :span="8" >用户名：</a-col>
        <a-col :span="10" >{{info.username}}</a-col>
      </a-row>
      <a-row type="flex" justify="start" style="margin-bottom: 20px">
        <a-col :span="8">管理员</a-col>
        <a-col :span="10">{{is_super}}</a-col>
      </a-row>
      <a-row type="flex" justify="start" style="margin-bottom: 20px">
        <a-col :span="8" >外网地址:</a-col>
        <a-col :span="10" >{{info.ha_url}}</a-col>
      </a-row>
      <a-row type="flex" justify="start">
        <a-col :span="8"   style="margin-bottom: 20px">访问密码:</a-col>
        <a-col :span="10" v-if="see===false"><a href="javascript:void(0)" @click="see = true"><a-icon type="eye-o" /></a></a-col>
        <a-col :span="10" v-if="see===true">{{info.ha_password}} &nbsp;&nbsp;<a href="javascript:void(0)" @click="see = false"><a-icon type="eye" /></a></a-col>
      </a-row>
      <a-row type="flex" justify="start">
        <a-col :span="8"   style="margin-bottom: 20px">当前状态: </a-col>
        <a-col :span="10" >{{info.is_active === true ? '已激活':'未激活'}}</a-col>
      </a-row>
      <a-row type="flex" justify="start">
        <a-col :span="8"   style="margin-bottom: 20px">注册日期: </a-col>
        <a-col :span="10" >{{info.date_joined}}</a-col>
      </a-row>
      <a-row type="flex" justify="start">
        <a-col :span="8"   style="margin-bottom: 20px">上次登录: </a-col>
        <a-col :span="10" >{{info.last_login}}</a-col>
      </a-row>
    </a-card>
    <a-modal
      title="补充对接信息"
      v-model="visible"
      @ok="hideModal"
      okText="确认"
      cancelText="取消"
    >
      <a-form>
        <a-form-item>
          <a-input placeholder="请输入HA外网地址" type="text" :defaultValue="info.ha_url" v-model="form.ha_url">
            <a-icon slot="prefix" type="global"/>
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-input placeholder="请输入HA访问密码" type="password" :defaultValue="info.ha_password" v-model="form.ha_password">
            <a-icon slot="prefix" type="lock"/>
          </a-input>
        </a-form-item>
      </a-form>
    </a-modal>
  </section>

</template>

<script>
/* eslint-disable no-unused-expressions */

import {ApiReq} from '../api'

export default {
  name: 'Profile',
  data () {
    return {
      title: '个人信息',
      info: {
      },
      see: false,
      modify: false,
      visible: false,
      form: {
        ha_url: '',
        ha_password: ''
      },
      info_modify: {
        password: '',
        password1: '',
        ha_url: '',
        ha_password: ''
      }
    }
  },
  methods: {
    date_parser (timeStr) {
      let oldTime = timeStr
      let d = oldTime.slice(0, 10)
      let t = oldTime.slice(11, -5)
      return d + ' ' + t
    },
    async refresh () {
      let that = this
      let res = await ApiReq(this, '/api/user_info')
      if (res && res.code === 0) {
        that.info = res.data
        that.info['last_login'] = that.date_parser(that.info['last_login'])
        that.info['date_joined'] = that.date_parser(that.info['date_joined'])
        if (that.info.ha_url === null) {
          that.visible = true
        }
      }
    },
    async hideModal () {
      let res = await ApiReq(this, '/api/modify_profile_info', this.form)
      if (res.code === 0) {
        this.visible = false
        this.$notification.success({
          message: '成功',
          description: res.msg
        })
      }
    }
  },
  async mounted () {
    await this.refresh()
  },
  computed: {
    is_super () {
      if (this.info.is_superuser === true) {
        return '是'
      } else {
        return '否'
      }
    }
  }
}
</script>

<style scoped>

</style>
