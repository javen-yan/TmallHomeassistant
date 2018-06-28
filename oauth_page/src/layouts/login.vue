<template>
  <div class="container">
    <div class="register-content">
      <a-card title="登陆" class="card-box">
        <a-form style="width: 66%; margin-left: 17%">
          <a-form-item>
            <a-input placeholder="请输入用户名" type="text" v-model="form.username">
              <a-icon slot="prefix" type="user"/>
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input placeholder="请输入密码" type="password" v-model="form.pw">
              <a-icon slot="prefix" type="lock"/>
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-row>
              <a-col :span="12">
                <a-button type='primary' @click="login">登陆</a-button>
              </a-col>
              <a-col :span="10">
                <a-button type='danger' @click="register">注册</a-button>
              </a-col>
            </a-row>
          </a-form-item>
        </a-form>
      </a-card>

    </div>
  </div>
</template>

<script>
import { ApiReq } from '../api'

export default {
  name: 'login',
  data () {
    return {
      form: {
        username: '',
        pw: ''
      }
    }
  },
  methods: {
    login: async function (e) {
      let res = await ApiReq(this, '/api/login', this.form)
      if (res.code === 0) {
        this.$notification.success({
          message: '成功',
          description: res.msg
        })
        window.localStorage.setItem('username', res.username)
        window.localStorage.setItem('sid', res.sid)
        window.localStorage.setItem('superuser', res.superuser)
        console.log(window.localStorage.getItem('path'))
        if (window.localStorage.getItem('path') !== null) {
          this.$router.push(window.localStorage.getItem('path'))
        } else {
          this.$router.push('/')
        }
      }
    },
    register (e) {
      this.$router.replace('/register')
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  background: #ececec;
  padding-top: 140px;
}
.card-box {
  width: 400px;
  margin: auto;
}
</style>
