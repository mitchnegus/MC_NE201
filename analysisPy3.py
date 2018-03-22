import matplotlib.pyplot as plt, numpy as np, matplotlib
matplotlib.rc('font', **{'size':14, 'family':'sans-serif'})
plt.rcParams['xtick.major.pad'] = '8'
plt.rcParams['ytick.major.pad'] = '8'
plt.rcParams['legend.fontsize'] = '12'


class flux_calc(object):
	
	def __init__(self):
		self.pallate = {'k':'#2c3e50', 'b':'#2980b9', 'r':'#c0392b', 'y':'#f39c12', 'p':'#8e44ad', 'g':'#27ae60',
						'gy':'#7f8c8d', 'o':'#d35400', 'w':'#ecf0f1', 'aq':'#16a085'}
	
	def get_energy_spectrum(self, E0_D2=102.6, Nps=1e5, dx=0.0, dy=0.0, dz=9.5, R_src=7.0, R_smpl=5.5, elbow=False):
		from numpy.random import rand, randn
		
		#constructing the energy and yield function
		A100, A200 = [2.46674, 0.30083, 0.01368, 0.0], [2.47685, 0.39111, 0.04098, 0.02957]
		B100, B200 = [0.01741, 0.88746, 0.22497, 0.08183, 0.37225], [-0.03149, 1.11225, 0.38659, 0.26676, 0.11518]
		coeffA = [A100[n] + (E0_D2-100.0) * (A200[n]-A100[n]) / 100.0 for n in range(4)]
		coeffB = [B100[n] + (E0_D2-100.0) * (B200[n]-B100[n]) / 100.0 for n in range(5)]
		eng_func = lambda theta_deg: coeffA[0] + sum([coeffA[n] * np.cos(theta_deg*np.pi/180.0)**n for n in range(1,4)])
		yield_func = lambda theta_deg: 1.0 + sum([coeffB[n] * np.cos(theta_deg*np.pi/180.0)**n for n in range(5)])
		
		#select src position (Gaussian)
		r_src, tht_src = R_src * 0.33 * randn(int(Nps)), 2.0 * np.pi * rand(int(Nps))
		xy_src = [(abs(r) * np.cos(tht_src[n]), abs(r) * np.sin(tht_src[n])) for n, r in enumerate(r_src)]
		
		#select sample position (uniform)
		r_smpl, tht_smpl = R_smpl * np.sqrt(rand(int(Nps))), 2.0 * np.pi * rand(int(Nps))
		xy_smpl = [(dx + r * np.cos(tht_smpl[n]), dy + r * np.sin(tht_smpl[n])) for n, r in enumerate(r_smpl)]
		
		#calculate angle/energy
		if elbow:
			angle_deg = [180.0 * np.arccos((dx-xy_smpl[n][0]) / np.sqrt((dz-s[0])**2 + (xy_smpl[n][1]-s[1])**2
						+ (dx-xy_smpl[n][0])**2)) / np.pi for n, s in enumerate(xy_src)]
		else:
			angle_deg = [180.0 * np.arccos(dz/np.sqrt((xy_smpl[n][0]-s[0])**2+(xy_smpl[n][1]-s[1])**2+dz**2))
						/ np.pi for n, s in enumerate(xy_src)]
		E_n = list(map(eng_func, angle_deg))
		
		#calculate weight
		dist = [np.sqrt(dz**2 + ((xy_smpl[n][0]-s[0])**2 + (xy_smpl[n][1]-s[1])**2)) for n, s in enumerate(xy_src)]
		wts = [yield_func(angle_deg[n]) / d**2 for n, d in enumerate(dist)]
		
		#sum wts
		hist, bin_edges = np.histogram(E_n, bins='auto')
		mu_E, sig_E, L = np.average(E_n), np.std(E_n), len(bin_edges)
		hist, unc = np.zeros(L-1), np.zeros(L-1)
		for n, e in enumerate(E_n):
			m = max((min((int(L*(0.5+(e-mu_E)/(6.0*sig_E))), L - 2)), 0))
			while bin_edges[m+1] < e and -1 < m < L:
				m += 1
			while bin_edges[m] >= e and -1 < m < L:
				m -= 1
			hist[m] += wts[n]
			unc[m] += wts[n]**2
		return bin_edges, hist / sum(hist), np.sqrt(unc) / sum(hist)

	def plot_energy_spectrum(self, dx=0.0, dy=0.0, dz=9.5, elbow=False, saveplot=False, space=0):
		#getting the energy spectrum
		edges, hist,unc = self.get_energy_spectrum(dx=dx, dy=dy, dz=dz, elbow=elbow)
		x, y = [], []
		for i in range(len(hist)):
			x.append(edges[i])
			x.append(edges[i+1])
			y.append(hist[i])
			y.append(hist[i])
		
		#getting and displaying the average and std of the neutron energy
		mu_E = (1.0/sum(hist)) * sum([0.5*(edges[n+1]+edges[n]) * h for n,h in enumerate(hist)])
		sig_E = np.sqrt((1.0/sum(hist)) * sum([h*(0.5*(edges[n]+edges[n+1])-mu_E)**2 for n,h in enumerate(hist)]))
		print('E =', round(mu_E,2), '+/-', round(sig_E,3), '[MeV]')
		
		#plotting the energy spectrum
		f, ax = plt.subplots()
		ax.plot(x, y, color=self.pallate['k'], lw=2.0)
		ax.errorbar([0.5*(e+edges[n+1]) for n, e in enumerate(edges[:-1])],
					hist, yerr=2.0 * unc, color=self.pallate['k'], ls='None', label='95% Confidence Bands')
		ymx = max(hist)
		ax.vlines(mu_E, ymin=0, ymax=ymx, colors=self.pallate['gy'], lw=2.0, label=r'$E_{average}$')
		ax.vlines([mu_E-sig_E,mu_E+sig_E], ymin=0, ymax=ymx, colors=self.pallate['gy'],
					lw=2.0, linestyles='--', label=r'$\pm 1\sigma_E$')
		ax.set_xlabel('Neutron Energy [MeV]')
		ax.set_ylabel('Flux [a.u.]')
		ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] + 0.008)
		ax.set_title('Neutron Flux in space {0}'.format(space))
		ax.legend(loc=0)
		f.tight_layout()
		if saveplot:
			f.savefig('plots/' + str(int(dx)) + str(int(dy)) + str(int(dz)) + str(elbow) + '.png')
		else:
			plt.show()
	
	def plot_all_sample_positions(self, saveplots=True):
		#iterate through all the spaces 
		for sm in [(0.0, 0.0, 9.5, False, 1), (9.0, 8.0, 9.5, False, 2), (18.0, 0.0, 9.5, False, 3), 
					(36.0, 0.0, 9.5, False, 4), (-7.0, 0.0, 46.0, True, 5)]:
			self.plot_energy_spectrum(dx=sm[0], dy=sm[1], dz=sm[2], elbow=sm[3], saveplot=saveplots, space=sm[4])
	"""
	def plot_energy_angle(self,deuteron_energy=102.6):
		A100,A200 = [2.46674,0.30083,0.01368,0.0],[2.47685,0.39111,0.04098,0.02957]
		coeff = [A100[n]+(deuteron_energy-100.0)*(A200[n]-A100[n])/100.0 for n in range(4)]
		f,ax = plt.subplots()
		eng_func = lambda theta_deg: coeff[0]+sum([coeff[n]*np.cos(theta_deg*np.pi/180.0)**n for n in range(1,4)])
		ax.plot(np.arange(0,180,0.1),[eng_func(t) for t in np.arange(0,180,0.1)],color=self.pallate['k'],lw=2.0,label=str(round(deuteron_energy,1))+' keV')
		ax.set_xlabel(r'$\theta$ [degrees]')
		ax.set_ylabel('Neutron Energy [MeV]')
		ax.legend(loc=0)
		f.tight_layout()
		plt.show()
	def plot_intensity_angle(self,deuteron_energy=102.6):
		B100,B200 = [0.01741,0.88746,0.22497,0.08183,0.37225],[-0.03149,1.11225,0.38659,0.26676,0.11518]
		coeffB = [B100[n]+(deuteron_energy-100.0)*(B200[n]-B100[n])/100.0 for n in range(5)]
		yield_func = lambda theta_deg: 1.0+sum([coeffB[n]*np.cos(theta_deg*np.pi/180.0)**n for n in range(5)])
		f,ax = plt.subplots()
		ax.plot(np.arange(0,180,0.1),[yield_func(t) for t in np.arange(0,180,0.1)],color=self.pallate['k'],lw=2.0,label=str(round(deuteron_energy,1))+' keV')
		ax.set_xlabel(r'$\theta$ [degrees]')
		ax.set_ylabel(r'R($\theta$)/R(90$^{\circ}$)')
		ax.legend(loc=0)
		f.tight_layout()
		plt.show()
	"""

if __name__=='__main__':
	fc = flux_calc()
	# fc.plot_energy_angle()
	# fc.plot_intensity_angle()
	# fc.plot_energy_spectrum()
	fc.plot_all_sample_positions(saveplots=False)