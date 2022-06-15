<template>
	<div style="height: 100%;">
		<el-menu
			default-active="$route.path"
			router
			class="el-menu-vertical-demo"
			:collapse="isCollapse"
		>
			<el-submenu index="">
				<template #title>
					<i class="el-icon-user-solid"></i>
					<span>用户</span>
				</template>
				<el-menu-item @click="logout"
					><i class="el-icon-switch-button"></i><span>退出</span></el-menu-item
				>
			</el-submenu>
			<el-menu-item index="/canvas">
				<i class="el-icon-files"></i>
				<template #title>仪表板</template>
			</el-menu-item>
			<el-menu-item index="/database">
				<i class="el-icon-coin"></i>
				<template #title>数据源</template>
			</el-menu-item>
		
			<el-menu-item index='updata'>
				<i class="el-icon-circle-plus"></i>
				<template #title>连接设置</template>
			</el-menu-item>
		</el-menu>
	</div>
</template>

<script>
export default {
	data() {
		return {
			isCollapse: true
		}
	},
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
		change() {}
	}
}
</script>
<style scoped>
.el-menu{
	max-height: 81.25rem;
	min-height: 6.25rem;
	height: 49.375rem;
	/* box-shadow: 1px 1px 10px #909090; */
	background-color: #2c3d59;
}
.el-icon-coin{
	/* background-color: ; */
}
</style>
