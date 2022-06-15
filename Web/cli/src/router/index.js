import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
  },
  {
    path: '/database',
    name: 'Database',
    component: () => import('@/views/Database.vue'),
  },
  {
    path: '/updata',
    name: 'Updata',
    component: () => import('@/views/Updata.vue')
  },
  {
    path:'/canvas',
    name:'Canvas',
    component: () => import('@/views/Canvas.vue')
  },
  
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to,form,next)=>{
  if(sessionStorage.getItem('username')!=null){
      if(to.name==='Login'){
        next('/database')
      }else{
        next()
      }
  }else{
    if(to.name==='Login'){
      next()
    }else{
      next()
    }
  }
})
export default router
