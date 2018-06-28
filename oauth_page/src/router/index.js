import Vue from 'vue'
import Router from 'vue-router'
import home from '@/layouts/home'
import register from '@/layouts/register'
import login from '@/layouts/login'
import Authorize from '@/layouts/authorize'
import Index from '@/pages/index'
import Profile from '@/pages/profile'
import Clients from '@/pages/clients'
import Devices from '@/pages/devices'
import Add from '@/pages/add'
import addVirtual from '@/pages/addVirtual'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: home,
      children: [
        {name: 'Index', path: '/', component: Index},
        {name: 'Profile', path: 'profile', component: Profile},
        {name: 'Clients', path: 'clients', component: Clients},
        {name: 'Devices', path: 'devices', component: Devices},
        {name: 'addVirtual', path: 'addVirtual', component: addVirtual},
        {name: 'Add', path: 'add', component: Add}
      ],
      beforeEnter: (to, from, next) => {
        if (window.localStorage.getItem('username') && window.localStorage.getItem('sid')) {
          next()
        } else {
          next({path: '/login'})
        }
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: register
    },
    {
      path: '/login',
      name: 'Login',
      component: login
    },
    {
      path: '/auth/:redirect_uri/:name/:scope',
      name: 'Authorize',
      component: Authorize
    }
  ]
})
