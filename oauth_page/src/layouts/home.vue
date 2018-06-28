<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout-sider
      :trigger="null"
      collapsible
      v-model="collapsed"
    >
      <a-icon
        class="trigger"
        :type="collapsed ? 'menu-unfold' : 'menu-fold'"
        @click="()=> collapsed = !collapsed"
      />
      <div class="logo">
        <img src="../../static/images/logo.png" style="width: 50%; height: 100%">
      </div>
      <a-menu theme="dark" mode="inline" :defaultSelectedKeys="['1']" @click="changeMenu">
        <a-menu-item key="1">
          <a-icon type="home" />
          <span>首页信息</span>
        </a-menu-item>
        <a-menu-item key="2">
          <a-icon type="profile" />
          <span>基础信息</span>
        </a-menu-item>
        <a-menu-item key="3" >
          <a-icon type="upload" />
          <span>设备管理</span>
        </a-menu-item>
        <a-menu-item key="4" v-show="is_superuser">
          <a-icon type="hdd" />
          <span>客户端管理</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <div class="login" v-if="is_login">
          <a-dropdown >
            <a class="ant-dropdown-link" href="#">
              <a-icon type="user" />{{username}} <a-icon type="down" />
            </a>
            <a-menu slot="overlay" @click="handleMenuClick">
              <a-menu-item key="1">个人信息</a-menu-item>
              <a-menu-item key="2">退出登录</a-menu-item>
            </a-menu>
          </a-dropdown>
        </div>
      </a-layout-header>
      <a-layout-content :style="{ margin: '24px 16px', padding: '24px', background: '#fff', overflow: 'initial'}">
        <router-view></router-view>
      </a-layout-content>
      <a-layout-footer style="textAlign: center">
        Geek-Ealine Design ©2018 Created by Ant UED
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script>

export default {
  name: 'home',
  data () {
    return {
      collapsed: true,
      is_login: false,
      username: 'Ealine',
      superuser: false
    }
  },
  methods: {
    changeMenu (item) {
      console.log(item)
      if (item.key === '1') {
        this.$router.replace('/')
      } else if (item.key === '2') {
        this.$router.replace('/profile')
      } else if (item.key === '3') {
        this.$router.replace('/devices')
      } else if (item.key === '4') {
        this.$router.replace('/clients')
      }
    },
    handleMenuClick (e) {
      if (e.key === '1') {
        this.$router.replace('/profile')
      } else if (e.key === '2') {
        window.localStorage.clear()
        this.$router.replace('/login')
      }
    }
  },
  mounted () {
    this.superuser = window.localStorage.getItem('superuser')
    this.username = window.localStorage.getItem('username')
    this.is_login = true
  },
  computed: {
    is_superuser () {
      return this.superuser === 'true'
    }
  }
}
</script>
<style>
#components-layout-demo-custom-trigger {
  height: 100%;
  width: 100%;
}

#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  margin: 16px;
  background: rgba(186, 255, 255, 0.2);
  text-align: center;
}
.login {
  float: right;
  margin-right: 30px;
}
</style>
