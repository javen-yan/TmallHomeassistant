<template>
  <div class="container">
    <div class="register-content">
      <a-card title="注册" :bordered="false" class="card-box">
        <a-form style="width: 66%; margin-left: 17%">
          <a-form-item>
            <a-input placeholder="请输入用户名" v-model="form.username">
              <a-icon slot="prefix" type="user" />
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input placeholder="请输入密码" type="password" v-model="form.pw">
              <a-icon slot="prefix" type="lock" />
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input placeholder="请再次输入"  type="password" v-model="form.pw1">
              <a-icon slot="prefix" type="lock" />
            </a-input>
          </a-form-item>
          <a-form-item>
               <a-button type='primary' @click="register">立即注册</a-button>
          </a-form-item>
        </a-form>
      </a-card>
    </div>
  </div>
</template>

<script>
import {ApiReq} from '../api'

export default {
  name: 'register',
  data () {
    return {
      form: {
        username: '',
        pw: '',
        pw1: ''
      }
    }
  },
  methods: {
    async register (e) {
      let res = await ApiReq(this, '/api/reg', this.form)
      if (res.code === 0) {
        this.$notification.success({
          message: '成功',
          description: res.msg
        })
        window.localStorage.setItem('username', res.username)
        window.localStorage.setItem('sid', res.sid)
        window.localStorage.setItem('superuser', res.superuser)
        this.$router.replace('/')
      }
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  background:#ECECEC;
  padding-top: 140px;
}
.card-box {
  width: 400px;
  margin: auto;
}
</style>
