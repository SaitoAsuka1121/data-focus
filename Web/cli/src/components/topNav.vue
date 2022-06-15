<template>
	<div style="height: 100%;">
		<el-menu default-active="$route.path" router></el-menu>
	</div>
</template>

<script>
export default {
	
	mounted() {
		if (sessionStorage.getItem('username') != null) {
			this.username = sessionStorage.getItem('username')
		}
	},
	methods: {
		
		logout() {
			this.$axios.get('/auth/logout').then(res => {
				console.log(res)
				if (res.data.code == 0) {
					sessionStorage.clear()
					this.$router.push('/')
				}
			})
		},
	}
}
</script>
<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
	height: 100%;
}
.heightAll {
	height: 100%;
}
</style>
